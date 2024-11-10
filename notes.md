# Project Notes

## 2024-11-09

- Got the right intersections and normals, but wrong sun direction and therefore wrong everything else
- Fixed sun direction - it's normalized direction w.r.t. eye it turns out.
- Still not working: sRGB final values are off compared to what the examples say.

### TODO

- Shadows are appearing in the wrong places (FIXED)
- Final values for sRGB are still a bit off

## 2024-11-10

- Implemented suns and expose successfully. sRGB still off, but the rest looks great
- Partially implemented view. The light is coming from the wrong side of the spheres after adjusting the perspective, but the spheres are placed correctly

### TODO

- Final values for sRGB are still a bit off
- ray-view case is showing light coming from the opposite side of the spheres that it should be (z-relative)