from pathlib import Path
import json, numpy as np
from simulate import run
root=Path(__file__).resolve().parents[1]
q,e,h,g=run(e=1.,damping=0.,air_drag=0.)
relative_energy_error=float(np.max(np.abs(e[120:]/e[120]-1)))
assert relative_energy_error<.002,relative_energy_error
q,e,h,g=run()
# Identify successive large excursions of either end after release.
a=np.max(abs(q[:,[0,4]]),axis=1)
peaks=[(k/120,float(a[k])) for k in range(122,len(a)-1) if a[k]>a[k-1] and a[k]>=a[k+1] and a[k]>.1]
assert len(peaks)>=12
assert peaks[-1][1]<peaks[0][1]
assert np.max(abs(q[:,1:4]))<.02
report={'ideal_limit_max_relative_energy_error':relative_energy_error,'free_motion_end_sphere_peaks':peaks,'maximum_middle_sphere_excursion_degrees':float(np.rad2deg(abs(q[:,1:4]).max())),'final_to_initial_mechanical_energy':float(e[-1]/e[120]),'checks_passed':True}
(root/'output/verification.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
