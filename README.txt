NEWTON'S CRADLE — 10 SECOND PHYSICS RENDER

Deliverables
  output/newtons_cradle.mp4     1920 x 1080, 30 fps, 300 frames, real-time playback
  output/newtons_cradle.blend   Editable Blender 4.5 scene and baked motion
  output/physics.json          Simulation parameters
  output/verification.json     Energy and amplitude checks

Scene
Five identical steel spheres on taut bifilar suspension wires, a stationary
machined base, walnut desktop, and a softly daylit office. The camera remains
fixed at a low tabletop viewpoint. No slow motion, camera animation, or added
artistic filters. The video is silent.

Motion and physical qualifications
0.0–0.8 s: prescribed external pull of the left sphere to 32.66 degrees.
0.8–1.0 s: held at rest. The pulling agent is outside the modeled scene.
1.0–10.0 s: free pendulum dynamics and rigid sphere contact impulses.
The spherical masses are 0.65 kg, radius 27 mm, with 235 mm pendulum length.
The integrator uses 60,000 steps/second. Restitution is 0.996, with linear
and quadratic angular drag. The middle spheres retain their small simulated
motions; they are not artificially frozen. Motion is baked at 120 Hz.

Taut strings must incline during a pendulum swing; permanently vertical
strings would contradict the requested motion. Both suspension points stay
fixed, and wire lengths remain constant. Near-elastic impulses transfer
momentum; mechanical energy gradually decreases through the specified losses.
The geometry is rigid, so microscopic elastic deformation, contact sound,
and string elasticity are not simulated.

Verification
With restitution set to 1 and drag removed, the maximum energy deviation
through the free-motion interval is 0.0053%. The rendered damped case has
18 successive end-sphere peaks; their amplitude drops from approximately
32.2 to 25.4 degrees. See the JSON reports for complete measurements.

Reproduction
Requires Blender 4.5 with Cycles; the render script selects an NVIDIA OptiX
GPU. Python simulation dependencies: numpy and numba.
  python scripts/simulate.py
  blender -b --python scripts/build_scene.py
  blender -b output/newtons_cradle.blend --python scripts/render.py
  python scripts/encode.py

Physics context
Virginia Tech, Newton's Cradle:
https://www.phys.vt.edu/outreach/projects-and-demos/demonstrations-wiki/mechanics/newtons-cradle.html
University of Maryland, Demo Highlight: Newton's Cradle:
https://lecdem.physics.umd.edu/tools-and-resources/lecdem-blog/541-demo-highlight-newton-s-cradle-blog.html

Repository and Git LFS
Clone this repository with Git LFS installed to retrieve the binary assets:
  git lfs install
  git clone https://github.com/alecjacobson/astra-newtons-cradle.git
  cd astra-newtons-cradle
  git lfs pull

Install Python dependencies before running the reproduction commands above:
  python -m pip install -r requirements.txt
The Python scripts run in your Python environment; the scene scripts use
Blender's bundled Python and require Blender 4.5 with NVIDIA OptiX support.

Git LFS stores the Blender scene, MP4, PNG preview, and NumPy binary data.
Source scripts, CSV motion samples, and verification reports use normal Git.
Intermediate frames, logs, Blender backups, and Python caches are ignored.
Rendering creates output/frames automatically and resumes existing frames.
Remove or move old frames before rendering a changed scene.

To rerun the existing physics and scene checks:
  python scripts/verify.py
  blender -b output/newtons_cradle.blend --python scripts/check_scene.py
After rendering, scripts/finalize.py can encode and validate the video and
package a source archive. It waits until all 300 frame images are present.
