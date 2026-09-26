import Foundation
import Metal

// Driver: read shared integer uniforms, count one session per GPU
// thread, write the per-session counts back to disk, print totals.
let args = CommandLine.arguments
guard args.count == 5 else {
    fputs("usage: gpudriver uniforms.bin out_new.bin out_differ.bin N\n", stderr)
    exit(2)
}
let uniPath = args[1]
let newPath = args[2]
let differPath = args[3]
guard let n = UInt32(args[4]) else { fatalError("bad N") }

guard let device = MTLCreateSystemDefaultDevice() else { fatalError("no Metal device") }
let metalURL = URL(fileURLWithPath: #file).deletingLastPathComponent().appendingPathComponent("count.metal")
let source = try String(contentsOf: metalURL, encoding: .utf8)
let lib = try device.makeLibrary(source: source, options: nil)
let pipe = try device.makeComputePipelineState(function: lib.makeFunction(name: "count_frames")!)

let uniData = try Data(contentsOf: URL(fileURLWithPath: uniPath))
let count = Int(n)
let uniBuf = device.makeBuffer(bytes: (uniData as NSData).bytes, length: uniData.count, options: .storageModeShared)!
let newBuf = device.makeBuffer(length: count * 4, options: .storageModeShared)!
let differBuf = device.makeBuffer(length: count * 4, options: .storageModeShared)!
var nn = n
let nBuf = device.makeBuffer(bytes: &nn, length: 4, options: .storageModeShared)!

let queue = device.makeCommandQueue()!
let cmd = queue.makeCommandBuffer()!
let enc = cmd.makeComputeCommandEncoder()!
enc.setComputePipelineState(pipe)
enc.setBuffer(uniBuf, offset: 0, index: 0)
enc.setBuffer(newBuf, offset: 0, index: 1)
enc.setBuffer(differBuf, offset: 0, index: 2)
enc.setBuffer(nBuf, offset: 0, index: 3)
enc.dispatchThreads(MTLSizeMake(count, 1, 1), threadsPerThreadgroup: MTLSizeMake(256, 1, 1))
enc.endEncoding()
cmd.commit()
cmd.waitUntilCompleted()
if let err = cmd.error { fatalError("gpu error: \(err)") }

let newPtr = newBuf.contents().bindMemory(to: UInt32.self, capacity: count)
let differPtr = differBuf.contents().bindMemory(to: UInt32.self, capacity: count)
var newTotal: UInt64 = 0
var differTotal: UInt64 = 0
for i in 0..<count {
    newTotal += UInt64(newPtr[i])
    differTotal += UInt64(differPtr[i])
}
try Data(bytes: newPtr, count: count * 4).write(to: URL(fileURLWithPath: newPath))
try Data(bytes: differPtr, count: count * 4).write(to: URL(fileURLWithPath: differPath))
let summary: [String: Any] = ["n": count, "new_total": newTotal, "differ_total": differTotal, "device": device.name]
print(String(data: try JSONSerialization.data(withJSONObject: summary), encoding: .utf8)!)
