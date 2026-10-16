from pathlib import Path
import numpy as np, json
from numba import njit
ROOT=Path(__file__).resolve().parents[1]
(ROOT/'output').mkdir(parents=True, exist_ok=True)
@njit
def run(e=.996, damping=.018, air_drag=.002):
    dt=1/60000.; L=.235; R=.027; mass=.65; n=600000
    q=np.zeros(5); w=np.zeros(5); samples=np.zeros((1201,5)); energy=np.zeros(1201)
    hits=np.zeros((3000,3)); nh=0; min_gap=0.; max_rise=0.
    for step in range(n+1):
        t=step*dt
        if t<.8:
            u=t/.8; q[0]=-.57*(10*u**3-15*u**4+6*u**5); w[0]=0.
        elif t<1.0:
            q[0]=-.57; w[0]=0.
        else:
            w+=(-9.81/L*np.sin(q)-damping*w-air_drag*w*np.abs(w))*dt
            q+=w*dt
            # Rigid, frictionless normal impulses, with exact pendulum tangent Jacobians.
            for iteration in range(5):
                for kk in range(4):
                    i=kk if iteration%2==0 else 3-kk; j=i+1
                    dx=2*R+L*(np.sin(q[j])-np.sin(q[i])); dz=L*(np.cos(q[i])-np.cos(q[j])); dist=np.sqrt(dx*dx+dz*dz)
                    gap=dist-2*R
                    if gap<min_gap:min_gap=gap
                    if gap<1e-9:
                        nx=dx/dist; nz=dz/dist
                        ai=nx*np.cos(q[i])+nz*np.sin(q[i]); aj=nx*np.cos(q[j])+nz*np.sin(q[j])
                        vrel=L*(aj*w[j]-ai*w[i]); den=ai*ai+aj*aj
                        if vrel<0:
                            imp=-(1+e)*vrel/den
                            w[i]-=imp*ai/L; w[j]+=imp*aj/L
                            if -vrel>.1 and nh<3000:
                                hits[nh]=[t,i,-vrel];nh+=1
                        if gap<0:
                            corr=-gap/den
                            q[i]-=corr*ai/L; q[j]+=corr*aj/L
        if step%500==0:
            k=step//500;samples[k]=q
            energy[k]=np.sum(.5*mass*(L*w)**2+mass*9.81*L*(1-np.cos(q)))
    return samples,energy,hits[:nh],min_gap
q,E,h,g=run()
np.savez(ROOT/'output/motion.npz',angles=q,energy=E,hits=h)
np.savetxt(ROOT/'output/angles.csv',q,delimiter=',')
report={'duration_seconds':10,'physics_step_seconds':1/60000,'animation_samples_hz':120,'sphere_radius_m':.027,'pendulum_length_m':.235,'mass_kg':.65,'restitution':.996,'release_seconds':1.0,'initial_angle_degrees':.57*180/np.pi,'minimum_gap_before_projection_m':float(g),'energy_at_release_j':float(E[120]),'energy_at_end_j':float(E[-1]),'number_of_resolved_impacts_above_0.1_m_s':len(h),'notes':'First 0.8 s is a prescribed external pull, then a 0.2 s hold. Subsequent motion is simulated. Normal impulses conserve momentum; small restitution loss and angular drag dissipate energy. Strings follow constrained pendulum arcs.'}
(ROOT/'output/physics.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
