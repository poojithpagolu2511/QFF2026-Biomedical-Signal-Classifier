# BioSignal Intelligence — Q1 Prototype v2

## Run on Windows
1. Extract this ZIP.
2. Open the folder in File Explorer; click the address bar, type `cmd`, press Enter.
3. Run `python -m pip install -r requirements.txt`
4. Run `python -m streamlit run app.py`
5. Open the local URL shown in the terminal, usually `http://localhost:8501`.

## Login
- **Create account / Sign in:** works locally; accounts are stored in `local_users.json`.
- **Google / GitHub:** add your own OAuth credentials by following `OAUTH_SETUP.md`. These providers will not work until their apps and callback URLs are configured.
- **Forgot password:** provider account recovery applies to Google/GitHub; local account password recovery is not implemented.

Do not publish `.streamlit/secrets.toml` or `local_users.json`. This is a local student prototype, not production-grade authentication.

## Features
- Biomedical-inspired navy/teal login screen
- Local account creation and sign-in
- Google/GitHub OAuth integration scaffold
- CSV upload, data preview, missing/duplicate checks, class distribution and numeric summary
- Classical Random Forest baseline, accuracy, confusion matrix and classification report
- Permutation feature importance, prediction studio and JSON/CSV exports
- Processor A/B JSON intake and readiness checklist
- No demo dataset included

## CSV
One row per sample/record; numeric columns are features; supervised classification needs a label column. Remove identifiers and use data you are licensed to use. Raw ECG/EEG may need segmentation and encoding according to the official Q1 Challenge Kit.

## Competition limitation
This is a classical ML baseline and experiment-preparation UI. It does NOT yet implement the official Q1 quantum classifier or execute on Processor A/B. Follow the official Challenge Kit for quantum method, inputs, processor definitions, runtime, metrics and submission. A professional UI cannot guarantee shortlisting.

## Safety
Educational only; not a medical device or diagnostic tool. Do not upload identifiable patient data.


## Login UI update
The login screen has been restyled to match the requested dark navy/teal BioSignal Intelligence concept, with a split hero/login layout and gradient sign-in action. Google and GitHub OAuth require credentials configured using `OAUTH_SETUP.md`.


## Login screen image
The sign-in screen uses the supplied BioSignal Intelligence image as the left-side hero artwork and renders real Streamlit sign-in/create-account controls on the right. Configure OAuth using `OAUTH_SETUP.md` for Google/GitHub buttons.


## Theme consistency update (V6)
The same dark navy and cyan/teal visual theme now continues after login across the sidebar, dashboard pages, metrics, data controls, buttons, tables and alerts.
\n\n## Professional copy update (V7)\nThe overview and navigation descriptions have been shortened and rewritten for a professional research prototype. Unnecessary promotional and repeated explanatory text has been removed.\n

## Feature upgrade (V8)
- Highlighted CSV upload area with matching neon cyan/teal theme.
- Icon-led sidebar navigation and section headings.
- Upload-derived CSV exports: dataset profile, numeric summary, and class distribution.
- Processor A/B configuration comparison and a two-row results template that includes both Processor A and Processor B.
- Processor result fields intentionally remain blank until actual official runs are performed; this avoids presenting simulated metrics as hardware results.
- All reports are downloadable as CSV files from the app.


## V9: configuration fixes and working local quantum simulation
- Processor qubit count accepts `num_qubits`, `qubits`, `n_qubits`, and `number_of_qubits`.
- Noise metadata accepts `noise_model`, `noise`, `noiseModel`, `error_rates`, and `noise_parameters`.
- Processor A/B page runs the same local NumPy statevector quantum feature map (RY rotations + CNOT entanglement) and Logistic Regression classifier on the uploaded dataset.
- Results include accuracy, weighted precision/recall/F1, run time, qubit count, feature map, and estimated circuit resource fields, with CSV and JSON downloads.
- This is a local simulator only: it does not access real quantum hardware, apply hardware noise, or substitute for the official Q1 Challenge Kit. Do not submit simulator results as hardware results.


## V10: prediction studio and upload reliability
- CSV upload state is only reset when the uploaded file contents change, preventing the model from being cleared on routine Streamlit reruns.
- Upload controls use a black button with a bright cyan border to stand out against the dark theme.
- Prediction Studio now supports input entry, predicted class display, class-probability charts and a downloadable probability CSV/JSON.
- Model evaluation includes weighted precision, recall and F1 in addition to accuracy.
- Reports include the held-out confusion matrix; feature traces handle empty/non-numeric values gracefully.
- Sidebar includes an icon legend and the Prediction Studio can guide the user back to Model Lab when a model has not yet been trained.
