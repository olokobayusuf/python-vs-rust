use std::os::raw::c_int;

#[no_mangle]
#[inline(never)]
pub extern "C" fn fma (x: f32, y: f32, z: f32, n_iter: c_int) -> f32 {
    let mut result = 0.0;
    for _ in 0..n_iter {
        result = x * y + z;
    }
    result
}