#include <metal_stdlib>
using namespace metal;

// One thread counts one session: sixteen steps of brain and finger
// arrivals from shared integer uniforms. The threshold, the held
// update, and the guess are identical to the CPU reference in
// gpurun.py, so the two counts must match elementwise.
kernel void count_frames(device const uint* uni [[buffer(0)]],
                         device uint* out_new [[buffer(1)]],
                         device uint* out_differ [[buffer(2)]],
                         constant uint& n [[buffer(3)]],
                         uint id [[thread_position_in_grid]]) {
    if (id >= n) {
        return;
    }
    const uint T = 1288490188u;
    bool held_fast = false;
    bool held_closed = false;
    uint nnew = 0;
    uint ndiff = 0;
    device const uint* u = uni + (uint64_t)id * 64u;
    for (uint s = 0; s < 16u; s++) {
        uint u0 = u[s * 4u + 0u];
        uint u1 = u[s * 4u + 1u];
        uint u2 = u[s * 4u + 2u];
        uint u3 = u[s * 4u + 3u];
        bool bmiss = u0 < T;
        bool fmiss = u1 < T;
        bool bv = (u2 & 1u) != 0u;
        bool fv = (u3 & 7u) == 0u;
        bool gfast = bmiss ? false : bv;
        bool gclosed = fmiss ? true : fv;
        bool sfast;
        bool sclosed;
        if (bmiss) {
            sfast = held_fast;
        } else {
            sfast = bv;
            held_fast = bv;
        }
        if (fmiss) {
            sclosed = held_closed;
        } else {
            sclosed = fv;
            held_closed = fv;
        }
        if (!bmiss && !fmiss) {
            nnew++;
        }
        if (gfast != sfast || gclosed != sclosed) {
            ndiff++;
        }
    }
    out_new[id] = nnew;
    out_differ[id] = ndiff;
}
