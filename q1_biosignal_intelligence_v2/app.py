import os,json,hmac,hashlib
import requests
from datetime import datetime
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_score,recall_score,f1_score
from sklearn.metrics import accuracy_score,classification_report,confusion_matrix,precision_score,recall_score,f1_score
from sklearn.inspection import permutation_importance

st.set_page_config(page_title="BioSignal Intelligence | Q1",page_icon="🧬",layout="wide")
st.markdown("""<style>
.stApp{background:linear-gradient(180deg,#f3f7fb,#f8fafc 55%,#edf3f9)}
.block-container{max-width:1450px;padding-top:1.2rem}
.hero{padding:1.7rem 2rem;border-radius:20px;background:linear-gradient(115deg,#101d35,#153e5a 60%,#176b75);color:white;margin-bottom:1.2rem;box-shadow:0 12px 32px #102b4718}
.hero h1{font-size:2.25rem;color:white;margin:.25rem 0}.hero p{color:#d9e8f5;margin:0}
.eyebrow{font-size:.72rem;font-weight:800;letter-spacing:.15em;color:#8ce0df}
[data-testid="stMetric"]{background:white;border:1px solid #dce5ef;padding:13px;border-radius:13px}
[data-testid="stSidebar"]{background:#eef3f9}
</style>""",unsafe_allow_html=True)
def hero(sub="Biomedical signal classification, model evaluation, and processor benchmarking in one workspace"):
 st.markdown(f"<div class='hero'><div class='eyebrow'>QISKIT FALL FEST 2026 · PHASE 1</div><h1>BioSignal Intelligence</h1><p>{sub}</p></div>",unsafe_allow_html=True)
def phash(p): return hashlib.sha256(p.encode()).hexdigest()
def users_read():
 try:
  with open("local_users.json",encoding="utf-8") as f:return json.load(f)
 except:return {}
def users_save(u):
 with open("local_users.json","w",encoding="utf-8") as f:json.dump(u,f,indent=2)
def oauth_login(provider):
 try:
  from streamlit_oauth import OAuth2Component
  cfg=st.secrets.get(provider,{})
  client_id=cfg.get("client_id",""); client_secret=cfg.get("client_secret","")
  if not client_id or not client_secret:
   st.warning(f"{provider.title()} sign-in needs OAuth credentials. See OAUTH_SETUP.md.")
   return
  if provider=="google":
   auth_url="https://accounts.google.com/o/oauth2/v2/auth"
   token_url="https://oauth2.googleapis.com/token"
   scope="openid email profile"
   user_url="https://openidconnect.googleapis.com/v1/userinfo"
  else:
   auth_url="https://github.com/login/oauth/authorize"
   token_url="https://github.com/login/oauth/access_token"
   scope="read:user user:email"
   user_url="https://api.github.com/user"
  oauth=OAuth2Component(client_id,client_secret,auth_url,token_url)
  result=oauth.authorize_button(
   name=f"Continue with {provider.title()}",
   redirect_uri=cfg.get("redirect_uri","http://localhost:8501"),
   scope=scope,
   key=f"oauth_{provider}",
   use_container_width=True
  )
  if result and result.get("token"):
   token=result["token"].get("access_token")
   if token:
    headers={"Authorization":f"Bearer {token}","Accept":"application/json"}
    response=requests.get(user_url,headers=headers,timeout=10);response.raise_for_status();profile=response.json()
    email=profile.get("email") or profile.get("login") or profile.get("sub") or profile.get("name")
    st.session_state.auth=True;st.session_state.username=f"{provider}:{email}";st.rerun()
 except Exception as e:
  st.error(f"{provider.title()} sign-in could not finish. Check the OAuth setup and redirect URI. Details: {e}")

def auth_screen():
 import base64
 from pathlib import Path
 hero_path=Path(__file__).parent/"assets"/"biosignal_login_hero.jpg"
 hero_b64=base64.b64encode(hero_path.read_bytes()).decode("ascii") if hero_path.exists() else ""
 st.markdown(f"""<style>
 .stApp{{background:radial-gradient(ellipse at 75% 15%,#062b42 0%,#031321 50%,#010813 100%);color:#eaf6ff}}
 [data-testid="stHeader"]{{background:transparent}}
 .block-container{{max-width:1600px;padding:0.6rem 1rem 1rem}}
 [data-testid="stToolbar"]{{right:1rem}}
 .login-brand{{font-size:2.15rem;font-weight:800;letter-spacing:-.045em;color:#f4fbff;line-height:1.15}}
 .login-brand span{{color:#18c9c2}}
 .login-sub{{color:#b5cfe0;font-size:1rem}}
 .login-panel{{padding:1.5rem 1.6rem 1.25rem;border:1px solid #087ab5;border-radius:27px;background:linear-gradient(145deg,rgba(3,19,35,.97),rgba(1,10,23,.98));box-shadow:0 0 34px #00b7ff22;}}
 .login-kicker{{letter-spacing:.2em;color:#38d8d0;font-weight:800;font-size:.72rem;padding:3px 0 22px}}
 .login-welcome{{font-size:2.35rem;font-weight:800;letter-spacing:-.035em;color:#f4fbff;margin:.9rem 0 .3rem}}
 .login-welcome span{{color:#18d2c4}}
 .login-desc{{color:#c0d5e4;margin-bottom:1.3rem;line-height:1.55}}
 [data-testid="stTextInput"] label{{color:#e7f4ff}}
 [data-testid="stTextInput"] input{{background:#06172a;color:#f3fbff;border:1px solid #285578;border-radius:13px;min-height:3.25rem}}
 [data-testid="stTextInput"] input:focus{{border-color:#22b8f0;box-shadow:0 0 0 1px #22b8f0}}
 [data-testid="stTabs"] button{{color:#b7d3e6}}
 [data-testid="stTabs"] [aria-selected="true"]{{color:#fff!important;border-bottom-color:#20d4c9!important}}
 div.stButton>button,div.stFormSubmitButton>button{{border-radius:12px;border:1px solid #216083;min-height:2.85rem;color:#f4fbff;background:#07192d}}
 div.stFormSubmitButton>button[kind="primary"],div.stButton>button[kind="primary"]{{background:linear-gradient(100deg,#075bea,#0bd0b2);border:0;color:white;font-weight:700}}
 .oauth-note{{color:#9ebbd0;text-align:center;margin:1rem 0 .4rem}}
 .fineprint{{font-size:.8rem;color:#8eacc2;margin-top:1.2rem}}
 .hero-image{{height:calc(100vh - 1.2rem);min-height:720px;background-image:url("data:image/jpeg;base64,{hero_b64}");background-position:center center;background-size:cover;background-repeat:no-repeat;border-radius:18px}}
 @media(max-width:900px){{.block-container{{padding:.5rem}}.hero-image{{height:480px;min-height:0;background-position:left center}}.login-panel{{padding:1rem}}.login-welcome{{font-size:1.8rem}}}}
 </style>""",unsafe_allow_html=True)
 left,right=st.columns([1.12,0.88],gap="large")
 with left:
  st.markdown('<div class="hero-image" aria-label="BioSignal Intelligence biomedical hero artwork"></div>',unsafe_allow_html=True)
 with right:
  st.markdown('<div class="login-panel"><div class="login-kicker">SECURE WORKSPACE</div>',unsafe_allow_html=True)
  signin,signup=st.tabs(["Sign in","Create account"])
  with signin:
   st.markdown('<div class="login-welcome">Welcome <span>Back</span></div><div class="login-desc">Sign in to your BioSignal Intelligence account<br>to continue exploring and analyzing biomedical signals.</div>',unsafe_allow_html=True)
   with st.form("login"):
    u=st.text_input("Email or Username",placeholder="Email or username")
    pw=st.text_input("Password",type="password",placeholder="Password")
    go=st.form_submit_button("Sign In  →",type="primary",use_container_width=True)
   if go:
    db=users_read()
    if u in db and hmac.compare_digest(db[u],phash(pw)):
     st.session_state.auth=True;st.session_state.username=u;st.rerun()
    else:st.error("Username or password is incorrect.")
   st.markdown('<div class="oauth-note">────────　or continue with　────────</div>',unsafe_allow_html=True)
   oa,gh=st.columns(2)
   with oa: oauth_login("google")
   with gh: oauth_login("github")
   with st.expander("Forgot password?"):
    st.caption("Password recovery for local accounts is not enabled yet. OAuth accounts are managed by Google or GitHub.")
   st.markdown('<div style="text-align:center;color:#c0d5e4;margin-top:1rem">Don’t have an account? Select <b>Create account</b> above.</div>',unsafe_allow_html=True)
  with signup:
   st.markdown('<div class="login-welcome">Create your <span>account</span></div><div class="login-desc">Create a local account to access your BioSignal Intelligence workspace.</div>',unsafe_allow_html=True)
   with st.form("signup"):
    nu=st.text_input("Username",placeholder="Choose a username")
    npw=st.text_input("Password (8+ characters)",type="password",placeholder="Create a password")
    cf=st.text_input("Confirm password",type="password",placeholder="Enter password again")
    create=st.form_submit_button("Create Account  →",type="primary",use_container_width=True)
   if create:
    db=users_read();nu=nu.strip()
    if len(nu)<3:st.error("Username must be at least 3 characters.")
    elif len(npw)<8:st.error("Password must be at least 8 characters.")
    elif npw!=cf:st.error("Passwords do not match.")
    elif nu in db:st.error("Username already exists.")
    else:db[nu]=phash(npw);users_save(db);st.success("Account created. Select Sign in and log in.")
  st.markdown('</div>',unsafe_allow_html=True)
  st.markdown('<div class="fineprint">Prototype access only · Do not upload identifiable patient data.</div>',unsafe_allow_html=True)

if not st.session_state.get("auth"):
 auth_screen();st.stop()
if "processor_configs" not in st.session_state:st.session_state.processor_configs={}
if "quantum_sim_results" not in st.session_state:st.session_state.quantum_sim_results=None

st.markdown("""<style>
/* Global BioSignal Intelligence dark theme for all pages after login */

.upload-callout{display:flex;align-items:center;gap:16px;padding:17px 20px;margin:8px 0 12px;border:1px solid #11c5dc;border-radius:16px;background:linear-gradient(100deg,#06314a,#09273d 60%,#063a42);box-shadow:0 0 22px #00cfe522}
.upload-icon{display:flex;align-items:center;justify-content:center;width:48px;height:48px;border-radius:13px;background:linear-gradient(140deg,#087cf5,#12d4bf);color:white;font-size:1.9rem;font-weight:800}
.upload-callout b{color:#f2fdff;font-size:1.08rem}.upload-callout span{color:#a8d6e9;font-size:.9rem}
[data-testid="stFileUploader"]{background:linear-gradient(135deg,#06243a,#071a2b)!important;border:2px dashed #13c5dc!important;border-radius:16px!important;padding:14px!important;box-shadow:inset 0 0 24px #00b9d41a}
[data-testid="stFileUploader"]:hover{border-color:#20e5d0!important;box-shadow:0 0 18px #00cfcf28}
[data-testid="stFileUploader"] button{border-radius:9px!important}
[data-testid="stFileUploader"] button{background:#020914!important;color:#f4fbff!important;border:1px solid #19d6df!important;font-weight:800!important;box-shadow:0 0 12px #00cfe522!important}
[data-testid="stFileUploader"] button:hover{background:#0a2538!important;border-color:#31f0e1!important}
.upload-callout{border-color:#12d9e2!important;background:linear-gradient(100deg,#020914,#071b2d 62%,#062d36)!important;box-shadow:0 0 26px #00d7e522!important}
.upload-icon{background:#020914!important;border:1px solid #18d9e2!important;color:#37eee5!important}


.stApp{background:radial-gradient(ellipse at 15% 0%,#0a2940 0%,#061525 42%,#020914 100%);color:#eaf6ff}
[data-testid="stHeader"]{background:rgba(2,9,20,.75)}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#071b2e,#030d1a);border-right:1px solid #123e5b}
[data-testid="stSidebar"] *{color:#e5f4ff}
[data-testid="stSidebar"] [data-testid="stRadio"] label{color:#d4e9f7}
.block-container{max-width:1450px;padding-top:1.35rem}
h1,h2,h3,h4,p,li,label,.stMarkdown{color:#e8f5ff}
[data-testid="stCaptionContainer"]{color:#9bbbd0}
[data-testid="stMetric"]{background:linear-gradient(145deg,#0b2439,#071729);border:1px solid #17415c;padding:14px;border-radius:14px}
[data-testid="stMetricLabel"]{color:#a8c9dd}
[data-testid="stMetricValue"]{color:#39d9d0}
[data-testid="stDataFrame"],[data-testid="stTable"]{background:#07192b;border:1px solid #17415c;border-radius:12px}
[data-testid="stFileUploader"]{background:#07192b;border:1px dashed #1a6484;border-radius:14px;padding:10px}
[data-testid="stTextInput"] input,[data-testid="stNumberInput"] input,[data-testid="stTextArea"] textarea{background:#06172a;color:#f3fbff;border:1px solid #285578;border-radius:10px}
[data-testid="stSelectbox"] div[data-baseweb="select"],[data-testid="stMultiSelect"] div[data-baseweb="select"]{background:#06172a;color:#eaf6ff}
div.stButton>button,div.stDownloadButton>button,div.stFormSubmitButton>button{background:linear-gradient(100deg,#075bea,#0bd0b2);border:1px solid #147caa;color:#fff;border-radius:11px;min-height:2.55rem;font-weight:650}
div.stButton>button:hover,div.stDownloadButton>button:hover{border-color:#37e1db;color:#fff;box-shadow:0 0 15px #08c5d322}
[data-testid="stTabs"] button{color:#a9c9dd}
[data-testid="stTabs"] [aria-selected="true"]{color:#fff!important;border-bottom-color:#20d4c9!important}
[data-testid="stAlert"]{background:#0a2438;border:1px solid #185271;color:#eaf6ff}
hr{border-color:#19435d}
[data-testid="stExpander"]{background:#07192b;border:1px solid #17415c;border-radius:12px}
</style>""",unsafe_allow_html=True)


def config_qubits(cfg):
 """Accept common qubit-count field names found in processor JSON schemas."""
 for key in ("num_qubits","qubits","n_qubits","number_of_qubits"):
  if key in cfg:
   val=cfg[key]
   if isinstance(val,list): return len(val)
   try: return int(val)
   except (TypeError,ValueError): pass
 return None

def config_noise(cfg):
 """Normalize noise metadata across common JSON field names."""
 for key in ("noise_model","noise","noiseModel","error_rates","noise_parameters"):
  if key in cfg: return key, cfg[key]
 return None, None

def normalized_edges(cfg,nq):
 raw=cfg.get("coupling_map",cfg.get("couplingMap",cfg.get("coupling",[])))
 edges=[]
 if isinstance(raw,dict):
  raw=raw.get("edges",[])
 if isinstance(raw,list):
  for e in raw:
   if isinstance(e,(list,tuple)) and len(e)>=2:
    try: a,b=int(e[0]),int(e[1])
    except (TypeError,ValueError): continue
    if 0<=a<nq and 0<=b<nq and a!=b: edges.append((a,b))
 return list(dict.fromkeys(edges))

def apply_ry(state,theta,q,nq):
 """Apply a single-qubit RY rotation to a pure statevector."""
 c=np.cos(theta/2); s=np.sin(theta/2); out=state.copy()
 bit=1<<q
 for base in range(0,1<<nq):
  if base & bit: continue
  i0=base; i1=base|bit
  a=state[i0]; b=state[i1]
  out[i0]=c*a-s*b
  out[i1]=s*a+c*b
 return out

def apply_cnot(state,control,target,nq):
 out=state.copy(); cb=1<<control; tb=1<<target
 for i in range(1<<nq):
  if (i&cb) and not (i&tb):
   j=i|tb; out[i]=state[j]; out[j]=state[i]
 return out

def quantum_feature_map(frame,nq,edges):
 """Small statevector quantum feature map. Returns computational-basis probabilities."""
 nq=max(1,min(int(nq),8))
 arr=frame.to_numpy(dtype=float)
 if arr.shape[1]==0: raise ValueError("Select at least one numeric feature.")
 mins=np.nanmin(arr,axis=0); maxs=np.nanmax(arr,axis=0)
 scale=np.where((maxs-mins)==0,1,maxs-mins)
 scaled=(arr-mins)/scale
 scaled=np.nan_to_num(scaled,nan=0.5,posinf=1.0,neginf=0.0)
 scaled=np.clip(scaled,0,1)
 out=[]
 use_edges=[(a,b) for a,b in edges if a<nq and b<nq]
 if not use_edges and nq>1: use_edges=[(q,q+1) for q in range(nq-1)]
 for row in scaled:
  state=np.zeros(1<<nq,dtype=np.complex128);state[0]=1.0
  for q in range(nq):
   angle=float(row[q%len(row)])*np.pi
   state=apply_ry(state,angle,q,nq)
  for a,b in use_edges:
   state=apply_cnot(state,a,b,nq)
  probs=np.abs(state)**2
  out.append(probs)
 return np.asarray(out), use_edges

def run_simulated_quantum_benchmark(df,label,features,config,processor_name,test_pct=25):
 """Run a reproducible local statevector simulation; this is not real hardware execution."""
 from sklearn.model_selection import train_test_split
 clean=df[features+[label]].replace([np.inf,-np.inf],np.nan).dropna().copy()
 clean[label]=clean[label].astype(str)
 if clean[label].nunique()<2 or clean[label].value_counts().min()<2:
  raise ValueError("Need at least two target classes and two complete samples per class.")
 qcount=config_qubits(config) or min(4,len(features))
 qcount=max(1,min(qcount,8))
 edges=normalized_edges(config,qcount)
 started=time.perf_counter()
 Xtr,Xte,ytr,yte=train_test_split(clean[features],clean[label],test_size=test_pct/100,random_state=42,stratify=clean[label])
 ptrain,used_edges=quantum_feature_map(Xtr,qcount,edges)
 ptest,_=quantum_feature_map(Xte,qcount,edges)
 clf=LogisticRegression(max_iter=1000,class_weight="balanced",random_state=42)
 clf.fit(ptrain,ytr);pred=clf.predict(ptest)
 elapsed=time.perf_counter()-started
 cfg_noise_key,cfg_noise=config_noise(config)
 n2=len(used_edges)
 metrics={
  "Processor":processor_name,
  "Execution mode":"Local statevector simulation (not hardware)",
  "Configuration name":config.get("name",config.get("backend_name",f"Processor {processor_name}")),
  "Qubits used":qcount,
  "Train samples":len(Xtr),"Test samples":len(Xte),
  "Accuracy":float(accuracy_score(yte,pred)),
  "Precision weighted":float(precision_score(yte,pred,average="weighted",zero_division=0)),
  "Recall weighted":float(recall_score(yte,pred,average="weighted",zero_division=0)),
  "F1 weighted":float(f1_score(yte,pred,average="weighted",zero_division=0)),
  "Feature map":"RY angle encoding + CNOT entanglement",
  "Two-qubit gates simulated":n2,
  "Circuit depth estimate":2 if n2 else 1,
  "Routing SWAPs":"Not modelled by this simulator",
  "Noise field detected":cfg_noise_key or "None",
  "Noise model applied":"No (metadata only)",
  "Runtime seconds":round(elapsed,6),
  "Random state":42
 }
 return metrics

with st.sidebar:
 st.markdown("## 🧬 BioSignal Intelligence")
 st.caption("Biomedical Signal Classification")
 st.write("Signed in: **"+st.session_state.get("username","team")+"**")
 if st.button("Sign out",use_container_width=True):st.session_state.clear();st.rerun()
 nav_items={
  "⌂  Overview":"Overview",
  "⇧  Upload & inspect":"Upload & inspect",
  "◈  Model lab":"Model lab",
  "⌁  Prediction studio":"Prediction studio",
  "▦  Processor A/B":"Processor A/B",
  "▤  Reports & readiness":"Reports & readiness",
 }
 nav_labels=list(nav_items.keys())
 requested_page=st.session_state.pop("_nav_request",None)
 default_nav=next((i for i,v in enumerate(nav_labels) if nav_items[v]==requested_page),0)
 selected_nav=st.radio("NAVIGATION",nav_labels,index=default_nav,key="main_navigation")
 page=nav_items[selected_nav]
 st.caption("ICON GUIDE")
 st.caption("⌂ Overview · ⇧ Upload · ◈ Train · ⌁ Predict · ▦ Processor comparison · ▤ Reports")
 st.divider();st.caption("Analyze · Evaluate · Compare")
hero()
def dataset_report_tables(d, label=None):
 """Create truthful, data-derived CSV reports for the uploaded dataset."""
 profile=pd.DataFrame({
  "column":d.columns.astype(str),
  "dtype":[str(x) for x in d.dtypes],
  "non_null_count":[int(d[c].notna().sum()) for c in d.columns],
  "missing_count":[int(d[c].isna().sum()) for c in d.columns],
  "missing_percent":[round(float(d[c].isna().mean()*100),2) for c in d.columns],
  "unique_values":[int(d[c].nunique(dropna=True)) for c in d.columns],
 })
 numeric=d.select_dtypes(include=np.number)
 numeric_summary=numeric.describe().T.reset_index().rename(columns={"index":"feature"})
 if label and label in d.columns:
  class_counts=d[label].astype(str).value_counts(dropna=False).rename_axis("class").reset_index(name="sample_count")
 else:
  class_counts=pd.DataFrame(columns=["class","sample_count"])
 return profile,numeric_summary,class_counts

def upload(key):
 st.markdown('<div class="upload-callout"><span class="upload-icon">⇧</span><div><b>Upload your biomedical dataset</b><br><span>CSV format · Black highlighted upload button · One sample per row</span></div></div>',unsafe_allow_html=True)
 f=st.file_uploader("Choose CSV dataset",type=["csv"],key=key,help="One sample per row. Include numeric feature columns and a target label for supervised classification.")
 if f:
  try:
   raw=f.getvalue()
   fingerprint=hashlib.sha256(raw).hexdigest()
   if st.session_state.get("dataset_fingerprint") != fingerprint:
    import io
    d=pd.read_csv(io.BytesIO(raw))
    if d.empty: st.error("CSV is empty.")
    else:
     st.session_state.df=d
     st.session_state.filename=f.name
     st.session_state.dataset_fingerprint=fingerprint
     for k in ("baseline","model","features","classes","quantum_sim_results","quantum_sim_time"):
      st.session_state.pop(k,None)
     st.session_state.label=None
     st.success(f"Dataset loaded: {len(d):,} rows · {len(d.columns)} columns. Model and report tools are ready.")
   elif st.session_state.get("df") is not None:
    st.caption(f"Loaded dataset: **{st.session_state.get('filename',f.name)}** · {len(st.session_state.df):,} rows")
  except Exception as e: st.error("Could not read CSV. Check that it is a valid, comma-separated table. Details: "+str(e))

if page=="Overview":
 st.subheader("🧭 Project Overview")
 st.markdown("Analyze biomedical feature data, evaluate a classification baseline, and prepare reproducible processor A/B experiments.")
 cs=st.columns(4)
 for c,n,t,d in zip(cs,["01","02","03","04"],["Data inspection","Classification","Model evaluation","Processor comparison"],["Review data quality","Train a baseline model","Measure predictive performance","Prepare A/B configurations"]):
  with c:
   st.markdown(f"### {n}")
   st.markdown(f"**{t}**")
   st.caption(d)
 d=st.session_state.get("df")
 if d is None:
  st.info("Upload a CSV dataset to begin analysis.")
 else:
  a,b,c,e=st.columns(4)
  a.metric("Dataset",st.session_state.get("filename","CSV")[:20])
  b.metric("Records",f"{len(d):,}")
  c.metric("Columns",len(d.columns))
  e.metric("Missing values",int(d.isna().sum().sum()))
 st.markdown("### 🗺️ Workflow")
 st.markdown("1. Upload and inspect your dataset.\n2. Select the target label and numeric features.\n3. Train and evaluate the baseline classifier.\n4. Load the official Processor A/B configurations and complete the benchmark using the challenge kit.")
 st.caption("Includes classical ML and a local statevector quantum simulation. Real QPU execution, device noise, and official Q1 challenge compliance still require the official Challenge Kit and authorized backend access.")

elif page=="Upload & inspect":
 st.subheader("📤 Dataset Inspection")
 st.caption("Upload a CSV to review its structure, completeness, class distribution, and numeric features.")
 upload("upload_inspection")
 d=st.session_state.get("df")
 if d is None:st.info("Choose your CSV above. No demo data is loaded.")
 else:
  a,b,c,e=st.columns(4);a.metric("Samples",f"{len(d):,}");b.metric("Fields",len(d.columns));c.metric("Missing cells",int(d.isna().sum().sum()));e.metric("Duplicate rows",int(d.duplicated().sum()))
  st.dataframe(d.head(20),use_container_width=True)
  default="label" if "label" in d.columns else d.columns[-1]
  label=st.selectbox("Target / label column",d.columns.tolist(),index=d.columns.tolist().index(default),key="label_inspect")
  st.session_state.label=label;num=d.drop(columns=[label]).select_dtypes(include=np.number)
  profile_csv,numeric_csv,classes_csv=dataset_report_tables(d,label)
  with st.expander("📦 Download generated dataset reports",expanded=True):
   r1,r2,r3=st.columns(3)
   with r1: st.download_button("⬇ Data profile CSV",profile_csv.to_csv(index=False),file_name="dataset_profile.csv",mime="text/csv",use_container_width=True)
   with r2: st.download_button("⬇ Numeric summary CSV",numeric_csv.to_csv(index=False),file_name="numeric_summary.csv",mime="text/csv",use_container_width=True)
   with r3: st.download_button("⬇ Class distribution CSV",classes_csv.to_csv(index=False),file_name="class_distribution.csv",mime="text/csv",use_container_width=True)
  l,r=st.columns(2)
  with l:
   st.markdown("#### Class distribution");counts=d[label].astype(str).value_counts(dropna=False)
   fig,ax=plt.subplots(figsize=(6,3));counts.plot(kind="bar",ax=ax);ax.set_ylabel("Samples");ax.tick_params(axis="x",rotation=25);fig.tight_layout();st.pyplot(fig);plt.close(fig)
  with r:
   st.markdown("#### Numeric summary")
   if len(num.columns):st.dataframe(num.describe().T,use_container_width=True)
   else:st.warning("No numeric feature columns found.")
  if len(num.columns):
   feat=st.selectbox("Feature trace",num.columns,key="inspect_feat")
   trace=pd.to_numeric(num[feat],errors="coerce").replace([np.inf,-np.inf],np.nan).dropna()
   if len(trace):
    fig,ax=plt.subplots(figsize=(9,2.7));ax.plot(trace.values[:1500],lw=1);ax.set_title(f"{feat} · first {min(1500,len(trace))} valid records");ax.set_xlabel("Record index");ax.set_ylabel("Feature value");ax.grid(alpha=.2);fig.tight_layout();st.pyplot(fig);plt.close(fig)
   else: st.warning(f"No valid numeric observations found for {feat}; choose another feature.")
  quality={"rows":len(d),"columns":len(d.columns),"missing_cells":int(d.isna().sum().sum()),"duplicate_rows":int(d.duplicated().sum()),"label":label,"classes":counts.to_dict(),"numeric_features":len(num.columns)}
  st.download_button("Export data quality report",json.dumps(quality,indent=2,default=str),file_name="data_quality_report.json",mime="application/json")
elif page=="Model lab":
 st.subheader("🧠 Model Lab · Classification")
 st.caption("Train a classical baseline and review its predictive performance.")
 upload("upload_model")
 d=st.session_state.get("df")
 if d is None:st.info("Upload a CSV above to unlock training.")
 else:
  default=st.session_state.get("label") or ("label" if "label" in d.columns else d.columns[-1])
  label=st.selectbox("Target label",d.columns.tolist(),index=d.columns.tolist().index(default) if default in d.columns else len(d.columns)-1,key="label_model")
  opts=d.drop(columns=[label]).select_dtypes(include=np.number).columns.tolist()
  feats=st.multiselect("Numeric feature columns",opts,default=opts);pct=st.slider("Test split (%)",20,40,25,5)
  if st.button("Train baseline & generate outputs",type="primary"):
   if not feats:st.error("Select at least one numeric feature.")
   else:
    clean=d[feats+[label]].replace([np.inf,-np.inf],np.nan).dropna();clean[label]=clean[label].astype(str)
    if clean[label].nunique()<2 or clean[label].value_counts().min()<2:st.error("Need at least two classes and two complete samples per class.")
    else:
     try:
      Xtr,Xte,ytr,yte=train_test_split(clean[feats],clean[label],test_size=pct/100,random_state=42,stratify=clean[label])
      model=make_pipeline(StandardScaler(),RandomForestClassifier(n_estimators=250,random_state=42,class_weight="balanced"))
      model.fit(Xtr,ytr);pred=model.predict(Xte);classes=sorted(clean[label].unique());cm=confusion_matrix(yte,pred,labels=classes)
      rep=classification_report(yte,pred,output_dict=True,zero_division=0)
      result={"model":"Classical Random Forest baseline","accuracy":float(accuracy_score(yte,pred)),"precision_weighted":float(precision_score(yte,pred,average="weighted",zero_division=0)),"recall_weighted":float(recall_score(yte,pred,average="weighted",zero_division=0)),"f1_weighted":float(f1_score(yte,pred,average="weighted",zero_division=0)),"train_samples":len(Xtr),"test_samples":len(Xte),"features":feats,"classes":classes,"confusion_matrix":cm.tolist(),"classification_report":rep,"timestamp":datetime.now().isoformat(timespec="seconds"),"random_state":42}
      st.session_state.baseline=result;st.session_state.model=model;st.session_state.features=feats;st.session_state.classes=classes
      a,b,c,e=st.columns(4);a.metric("Test accuracy",f"{result['accuracy']:.1%}");b.metric("Weighted precision",f"{result['precision_weighted']:.1%}");c.metric("Weighted recall",f"{result['recall_weighted']:.1%}");e.metric("Weighted F1",f"{result['f1_weighted']:.1%}")
      st.caption(f"Split: {len(Xtr):,} training rows / {len(Xte):,} test rows · Random seed: 42")
      l,r=st.columns(2)
      with l:
       st.markdown("#### Confusion matrix");fig,ax=plt.subplots(figsize=(5,4));im=ax.imshow(cm);ax.set_xticks(range(len(classes)),labels=classes,rotation=35,ha="right");ax.set_yticks(range(len(classes)),labels=classes);ax.set_xlabel("Predicted");ax.set_ylabel("Actual")
       for i in range(len(classes)):
        for j in range(len(classes)):ax.text(j,i,str(cm[i,j]),ha="center",va="center")
       fig.colorbar(im,ax=ax);fig.tight_layout();st.pyplot(fig);plt.close(fig)
      with r:st.markdown("#### Classification report");st.dataframe(pd.DataFrame(rep).T,use_container_width=True)
      try:
       imp=permutation_importance(model,Xte,yte,n_repeats=8,random_state=42,scoring="accuracy")
       importance=pd.DataFrame({"Feature":feats,"Importance":imp.importances_mean}).sort_values("Importance",ascending=False)
       st.markdown("#### Explainability · permutation feature importance");fig,ax=plt.subplots(figsize=(8,3.5));ax.barh(importance.Feature[::-1],importance.Importance[::-1]);ax.set_xlabel("Accuracy decrease when shuffled");fig.tight_layout();st.pyplot(fig);plt.close(fig)
       st.download_button("Download feature importance CSV",importance.to_csv(index=False),file_name="feature_importance.csv",mime="text/csv")
      except Exception:pass
      st.success("Baseline complete. These are classical ML results, not quantum results.")
     except Exception as e:st.error("Training failed: "+str(e))
 if st.session_state.get("baseline"):st.download_button("Download metrics JSON",json.dumps(st.session_state.baseline,indent=2),file_name="classical_baseline_metrics.json",mime="application/json")
elif page=="Prediction studio":
 st.subheader("🔎 Prediction Studio")
 st.caption("Enter one sample's feature values to classify it with your trained model and inspect its class probabilities.")
 d=st.session_state.get("df");model=st.session_state.get("model");feats=st.session_state.get("features")
 if d is None or model is None:
  st.warning("No trained model is available yet. Upload a labeled CSV, open Model Lab, select the target and features, then train the baseline.")
  if st.button("Go to Model Lab",type="primary"): st.session_state["_nav_request"]="Model lab";st.rerun()
 else:
  st.success(f"Model ready · {len(feats)} features · trained on the current dataset")
  with st.form("prediction"):
   vals={};cs=st.columns(2)
   for i,f in enumerate(feats):
    series=pd.to_numeric(d[f],errors="coerce").replace([np.inf,-np.inf],np.nan).dropna()
    median=float(series.median()) if len(series) else 0.0
    minimum=float(series.min()) if len(series) else median-1
    maximum=float(series.max()) if len(series) else median+1
    with cs[i%2]:
     vals[f]=st.number_input(f"{f}",value=median,help=f"Observed dataset range: {minimum:.4g} to {maximum:.4g}",format="%.6f")
   go=st.form_submit_button("✨ Classify sample",type="primary",use_container_width=True)
  if go:
   row=pd.DataFrame([vals],columns=feats)
   try:
    pred=str(model.predict(row)[0])
    st.success("Predicted dataset class: "+pred)
    probs=None
    try:
     probs=model.predict_proba(row)[0]
     classes=list(model.classes_)
     prob_df=pd.DataFrame({"Class":classes,"Probability":probs})
     st.markdown("### 📊 Prediction confidence by class")
     fig,ax=plt.subplots(figsize=(8,3.5))
     ax.bar(prob_df["Class"].astype(str),prob_df["Probability"])
     ax.set_ylim(0,1);ax.set_ylabel("Model probability");ax.set_xlabel("Dataset class");ax.tick_params(axis="x",rotation=25);ax.grid(axis="y",alpha=.2)
     fig.tight_layout();st.pyplot(fig);plt.close(fig)
     st.dataframe(prob_df,use_container_width=True,hide_index=True)
     st.download_button("⬇ Download class probabilities CSV",prob_df.to_csv(index=False),file_name="prediction_probabilities.csv",mime="text/csv")
    except Exception: pass
    prediction={"prediction":pred,"input":vals,"model":"Classical Random Forest baseline","class_probabilities":dict(zip(map(str,model.classes_),map(float,probs))) if probs is not None else None,"note":"Prediction is based on the uploaded dataset and trained model; it is not a medical diagnosis.","timestamp":datetime.now().isoformat()}
    st.download_button("⬇ Download prediction JSON",json.dumps(prediction,indent=2),file_name="prediction.json",mime="application/json")
   except Exception as e: st.error("Prediction failed: "+str(e))

elif page=="Processor A/B":
 st.subheader("⚛️ Processor A/B Comparison")
 st.markdown("Run the same **local quantum statevector simulation** against both processor configurations, using the uploaded dataset and matching train/test settings.")
 st.info("This provides a working simulated quantum-classification experiment. It is not real QPU execution and does not apply hardware noise. Use the official Q1 Challenge Kit before treating results as hackathon-compliant.")
 ca,cb=st.columns(2)
 for col,n in [(ca,"A"),(cb,"B")]:
  with col:
   st.markdown(f"#### {'🔹' if n=='A' else '🔸'} Processor {n}")
   f=st.file_uploader(f"Upload Processor {n} JSON",type=["json"],key="proc"+n)
   if f:
    try:
     cfg=json.load(f)
     if not isinstance(cfg,dict): raise ValueError("Processor JSON must contain an object.")
     st.session_state.processor_configs[n]=cfg
     st.success(f"Processor {n} configuration loaded.")
     nq=config_qubits(cfg)
     noise_key,noise_val=config_noise(cfg)
     st.metric("Qubits detected",nq if nq is not None else "Not specified")
     st.caption(f"Noise metadata: {noise_key or 'not specified'}")
     with st.expander(f"View Processor {n} JSON"): st.json(cfg)
    except Exception as e:st.error("Invalid processor JSON: "+str(e))
 cfgs=st.session_state.processor_configs
 if cfgs:
  rows=[]
  for n,x in cfgs.items():
   nq=config_qubits(x);edges=normalized_edges(x,nq or 10000)
   noise_key,noise_val=config_noise(x)
   gates=x.get("basis_gates",x.get("basisGates",[]))
   rows.append({"Processor":f"Processor {n}","Configuration name":x.get("name",x.get("backend_name","Not specified")),
    "Qubits":nq if nq is not None else "Not specified",
    "Coupling edges":len(edges),
    "Basis gates":", ".join(gates) if isinstance(gates,list) else str(gates),
    "Noise field":noise_key or "Not specified",
    "Noise metadata present":"Yes" if noise_key else "No"})
  config_df=pd.DataFrame(rows)
  st.markdown("### 📋 Configuration comparison")
  st.dataframe(config_df,use_container_width=True,hide_index=True)
  st.download_button("⬇ Export configuration comparison CSV",config_df.to_csv(index=False),file_name="processor_A_B_configuration_comparison.csv",mime="text/csv")
 else:
  st.caption("Upload the official JSON configuration for each processor. Common fields such as `qubits`, `num_qubits`, `noise_model`, and `noise` are recognized.")
 st.markdown("### 🧪 Run the simulated quantum experiment")
 d=st.session_state.get("df")
 if d is None:
  st.warning("First upload your dataset from **Upload & inspect** or **Model lab**.")
 elif not ("A" in cfgs and "B" in cfgs):
  st.warning("Upload both Processor A and Processor B JSON files to enable the paired experiment.")
 else:
  default=st.session_state.get("label") or ("label" if "label" in d.columns else d.columns[-1])
  target_options=d.columns.tolist()
  label=st.selectbox("Target / class label",target_options,index=target_options.index(default) if default in target_options else len(target_options)-1,key="qsim_label")
  numeric_features=d.drop(columns=[label]).select_dtypes(include=np.number).columns.tolist()
  features=st.multiselect("Numeric input features",numeric_features,default=numeric_features[:min(6,len(numeric_features))],key="qsim_features")
  test_pct=st.slider("Test split (%)",20,40,25,5,key="qsim_testpct")
  st.caption("For reproducibility, both processors use the same data split seed (42), selected features, target, and test percentage.")
  if st.button("🚀 Run Processor A + B simulation",type="primary",use_container_width=True):
   if not features: st.error("Select at least one numeric feature.")
   else:
    try:
     results=[]
     for n in ("A","B"):
      metrics=run_simulated_quantum_benchmark(d,label,features,cfgs[n],n,test_pct)
      metrics["Dataset"]=st.session_state.get("filename","uploaded.csv")
      metrics["Target label"]=label
      metrics["Selected features"]="; ".join(features)
      results.append(metrics)
     results_df=pd.DataFrame(results)
     st.session_state.quantum_sim_results=results_df
     st.session_state.quantum_sim_time=datetime.now().isoformat(timespec="seconds")
     st.success("Both local simulation runs completed.")
    except Exception as e: st.error("Simulation failed: "+str(e))
 if st.session_state.get("quantum_sim_results") is not None:
  result_df=st.session_state.quantum_sim_results
  st.markdown("### 📈 Simulation results")
  m1,m2,m3,m4=st.columns(4)
  m1.metric("Processor A accuracy",f"{float(result_df.iloc[0]['Accuracy']):.1%}")
  m2.metric("Processor B accuracy",f"{float(result_df.iloc[1]['Accuracy']):.1%}")
  m3.metric("A/B accuracy difference",f"{abs(float(result_df.iloc[0]['Accuracy'])-float(result_df.iloc[1]['Accuracy'])):.1%}")
  m4.metric("Features selected",len(st.session_state.get("qsim_features",[])))
  st.dataframe(result_df,use_container_width=True,hide_index=True)
  st.download_button("⬇ Download Processor A/B simulation results CSV",result_df.to_csv(index=False),file_name="processor_A_B_simulation_results.csv",mime="text/csv",type="primary")
  st.download_button("⬇ Download simulation report JSON",json.dumps({"run_time":st.session_state.get("quantum_sim_time"),"results":result_df.to_dict(orient="records"),"disclaimer":"Local statevector simulation only; not actual QPU execution and not official challenge evidence."},indent=2,default=str),file_name="processor_A_B_simulation_report.json",mime="application/json")
 st.markdown("### 📄 Manual results template")
 template=pd.DataFrame([
  {"Processor":"A","Execution mode":"Pending","Dataset":"", "Model / circuit":"", "Accuracy":"", "Precision":"", "Recall":"", "F1 score":"", "Circuit depth":"", "Two-qubit gates":"", "SWAP count":"", "Runtime seconds":"", "Notes":"Enter actual hardware results only when available."},
  {"Processor":"B","Execution mode":"Pending","Dataset":"", "Model / circuit":"", "Accuracy":"", "Precision":"", "Recall":"", "F1 score":"", "Circuit depth":"", "Two-qubit gates":"", "SWAP count":"", "Runtime seconds":"", "Notes":"Use same inputs and settings as Processor A."},
 ])
 st.download_button("⬇ Download manual Processor A + B CSV template",template.to_csv(index=False),file_name="processor_A_B_results_template.csv",mime="text/csv")
 if d is not None:
  profile,numeric,classes=dataset_report_tables(d,st.session_state.get("label"))
  st.markdown("### ✨ Dataset-linked exports")
  pack=st.columns(3)
  with pack[0]: st.download_button("⬇ Dataset profile",profile.to_csv(index=False),file_name="dataset_profile.csv",mime="text/csv",use_container_width=True,key="proc_profile")
  with pack[1]: st.download_button("⬇ Feature summary",numeric.to_csv(index=False),file_name="numeric_summary.csv",mime="text/csv",use_container_width=True,key="proc_numeric")
  with pack[2]: st.download_button("⬇ Class counts",classes.to_csv(index=False),file_name="class_distribution.csv",mime="text/csv",use_container_width=True,key="proc_classes")

else:
 st.subheader("📊 Reports & Readiness")
 res=st.session_state.get("baseline")
 if res:
  a,b,c,e=st.columns(4);a.metric("Baseline accuracy",f"{res['accuracy']:.1%}");b.metric("Weighted precision",f"{res.get('precision_weighted',0):.1%}");c.metric("Weighted recall",f"{res.get('recall_weighted',0):.1%}");e.metric("Weighted F1",f"{res.get('f1_weighted',0):.1%}")
  st.caption(f"Evaluation used {res['test_samples']} held-out samples and {len(res['features'])} numeric features.")
  if res.get("confusion_matrix") and res.get("classes"):
   cm=np.asarray(res["confusion_matrix"]);classes=res["classes"]
   fig,ax=plt.subplots(figsize=(5,4));im=ax.imshow(cm);ax.set_title("Held-out confusion matrix");ax.set_xticks(range(len(classes)),labels=classes,rotation=30,ha="right");ax.set_yticks(range(len(classes)),labels=classes);ax.set_xlabel("Predicted class");ax.set_ylabel("Actual class")
   for ii in range(len(classes)):
    for jj in range(len(classes)):ax.text(jj,ii,str(cm[ii,jj]),ha="center",va="center")
   fig.colorbar(im,ax=ax);fig.tight_layout();st.pyplot(fig);plt.close(fig)
 else:st.info("Run the baseline to add its metrics to this report.")
 tasks=["Exactly one problem statement selected","Official Q1 Challenge Kit inputs used","Quantum Q1 method implemented","Processor A run completed","Processor B run completed","Same settings on A and B","Problem-specific metrics recorded","Architecture/resource metrics recorded","Tables and figures saved","README/environment specification prepared","Clean reproducible run verified","AI assistance disclosed if required"]
 done=[st.checkbox(t,key="ready_"+t,value=t=="README/environment specification prepared") for t in tasks]
 st.metric("Readiness checklist",f"{sum(done)}/{len(tasks)}")
 out={"project":"BioSignal Intelligence Q1 prototype","created_at":datetime.now().isoformat(timespec="seconds"),"dataset":st.session_state.get("filename"),"baseline":res,"processor_configs_loaded":list(st.session_state.processor_configs.keys()),"readiness":dict(zip(tasks,done))}
 st.download_button("Export experiment status JSON",json.dumps(out,indent=2,default=str),file_name="experiment_status.json",mime="application/json")
st.divider();st.caption("Research prototype · Not intended for clinical diagnosis · Do not upload identifiable patient data.")
