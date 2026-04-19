document.addEventListener('DOMContentLoaded', () => {
    // --- UI ELEMENTS ---
    const scanBtn = document.getElementById('scanBtn');
    const logConsole = document.getElementById('logConsole');
    const progressBar = document.getElementById('progressBar');
    const progressText = document.getElementById('progressText');
    const progressDetail = document.getElementById('progressDetail');
    const reportList = document.getElementById('reportList');
    const payloadList = document.getElementById('payloadList');
    const vulnCount = document.getElementById('vulnCount');
    const targetCountText = document.getElementById('targetCount');
    const systemStatus = document.getElementById('systemStatus');
    const secLevelPill = document.getElementById('secLevelPill');
    const targetPathInput = document.getElementById('targetPath');
    const browseFolderBtn = document.getElementById('browseFolderBtn');
    const browseFileBtn = document.getElementById('browseFileBtn');

    // --- INITIALIZATION ---
    fetchReports();
    fetchPayloads();

    // --- NATIVE FILE EXPLORER LOGIC ---
    async function callNativePicker(mode) {
        try {
            if (systemStatus) {
                systemStatus.innerText = `WAITING FOR ${mode.toUpperCase()} PICKER...`;
                systemStatus.style.color = '#ffee00';
            }
            
            const response = await fetch(`/api/browse-native?mode=${mode}`);
            const data = await response.json();
            
            if (data.path && targetPathInput) {
                targetPathInput.value = data.path;
                addLog(`Đã chọn: ${data.path}`, '#00f5ff');
            }
        } catch (err) {
            console.error('Native picker failed:', err);
            addLog('Không thể mở trình chọn hệ thống.', '#ff3131');
        } finally {
            if (systemStatus) {
                systemStatus.innerText = 'SYSTEM READY';
                systemStatus.style.color = 'var(--neon-cyan)';
            }
        }
    }

    if (browseFolderBtn) browseFolderBtn.addEventListener('click', () => callNativePicker('folder'));
    if (browseFileBtn) browseFileBtn.addEventListener('click', () => callNativePicker('file'));

    // --- SCAN LOGIC (REAL-TIME STREAMING) ---
    if (scanBtn) {
        scanBtn.addEventListener('click', async () => {
            const path = targetPathInput ? targetPathInput.value : '';
            const ai = document.getElementById('aiToggle') ? document.getElementById('aiToggle').checked : false;
            const pwn = document.getElementById('pwnToggle') ? document.getElementById('pwnToggle').checked : false;
            const groqKey = document.getElementById('groqApiKey') ? document.getElementById('groqApiKey').value : '';

            if (!path) {
                alert('Vui lòng chọn hoặc nhập đường dẫn mục tiêu!');
                return;
            }

            // Reset UI & Stats
            if (logConsole) logConsole.innerHTML = '';
            if (reportList) reportList.innerHTML = ''; 
            if (vulnCount) vulnCount.innerText = '0';
            if (targetCountText) targetCountText.innerText = '0';
            
            let currentFindings = 0;
            let totalTargets = 0;
            
            addLog('Initiating APS Strategic Audit...', '#00f5ff');
            addLog(`Target: ${path}`, '#94a3b8');
            
            updateProgress(5, 'Initializing stream...');
            scanBtn.disabled = true;
            if (systemStatus) {
                systemStatus.innerText = 'STATUS: AUDIT IN PROGRESS';
                systemStatus.style.color = '#ffee00';
            }
            resetLayers();

            try {
                const response = await fetch('/api/scan', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ path, ai, pwn, groqKey })
                });

                const reader = response.body.getReader();
                const decoder = new TextDecoder();
                let buffer = '';
                
                while (true) {
                    const { value, done } = await reader.read();
                    if (done) break;
                    
                    buffer += decoder.decode(value, { stream: true });
                    const parts = buffer.split('\n\n');
                    buffer = parts.pop(); 
                    
                    for (const part of parts) {
                        const lines = part.split('\n');
                        for (const line of lines) {
                            if (line.trim().startsWith('data: ')) {
                                try {
                                    const data = JSON.parse(line.trim().substring(6));
                                    handleStreamEvent(data);
                                } catch (e) {
                                    console.error("Stream parse error:", e, line);
                                }
                            }
                        }
                    }
                }

                function handleStreamEvent(data) {
                    if (data.event === 'start') {
                        totalTargets = data.total;
                        if (targetCountText) targetCountText.innerText = `0 / ${totalTargets}`;
                        addLog(`Detected ${totalTargets} strategic targets.`, '#ffee00');
                    } 
                    else if (data.event === 'file_start') {
                        addLog(`Processing [${data.index}/${totalTargets}]: ${data.target}`, '#94a3b8');
                    }
                    else if (data.event === 'file_result') {
                        const res = data.result;
                        const index = data.index;
                        const pct = Math.round((index / totalTargets) * 100);
                        
                        updateProgress(pct, `SCANNING [${index}/${totalTargets}]`);
                        if (targetCountText) targetCountText.innerText = `${index} / ${totalTargets}`;
                        
                        if (res.results) {
                            Object.values(res.results).forEach(section => {
                                if (Array.isArray(section)) currentFindings += section.length;
                            });
                        }
                        if (vulnCount) vulnCount.innerText = currentFindings;
                        updateSecurityLevel(currentFindings);
                        appendReportItem(res.report_path, res.target);
                        flashLayerProgress(index);
                    }
                    else if (data.event === 'finish') {
                        updateProgress(100, 'Mission completed. Strategic reports finalized.');
                        addLog(`Found ${currentFindings} vulnerabilities across ${totalTargets} targets.`, '#00f5ff');
                    }
                    else if (data.event === 'error' || data.event === 'file_error') {
                        addLog(`[ERROR] ${data.error}`, '#ff3131');
                    }
                }

            } catch (error) {
                addLog(`[SYSTEM FAILURE] ${error.message}`, '#ff3131');
            } finally {
                scanBtn.disabled = false;
                if (systemStatus) {
                    systemStatus.innerText = 'SYSTEM READY';
                    systemStatus.style.color = 'var(--neon-cyan)';
                }
                fetchPayloads(); 
            }
        });
    }

    // --- HELPER FUNCTIONS ---
    function appendReportItem(filename, fullpath) {
        if (!reportList) return;
        const basename = filename.split('/').pop();
        const li = document.createElement('li');
        li.innerHTML = `
            <div class="item-info">
                <span class="item-name" title="${basename}">${basename.split('.')[0]}</span>
                <small style="color:var(--text-dim); font-size:0.65rem;">Source: ${fullpath}</small>
            </div>
            <a href="/reports/${basename}" target="_blank">OPEN</a>
        `;
        reportList.insertBefore(li, reportList.firstChild);
    }

    function updateSecurityLevel(findings) {
        if (!secLevelPill) return;
        if (findings > 15) {
            secLevelPill.innerText = 'STATUS: CRITICAL';
            secLevelPill.style.background = 'rgba(255, 49, 49, 0.1)';
            secLevelPill.style.color = 'var(--neon-red)';
        } else if (findings > 0) {
            secLevelPill.innerText = 'STATUS: WARNING';
            secLevelPill.style.background = 'rgba(255, 238, 0, 0.1)';
            secLevelPill.style.color = 'var(--neon-yellow)';
        }
    }

    function flashLayerProgress(index) {
        const layers = document.querySelectorAll('.layer-item');
        if (layers.length === 0) return;
        const randomLayer = layers[index % layers.length];
        const status = randomLayer.querySelector('.l-status');
        if (status) {
            status.innerText = 'VERIFYING...';
            status.className = 'l-status status-active';
            setTimeout(() => {
                status.innerText = 'DONE';
                status.className = 'l-status status-done';
            }, 800);
        }
    }

    function addLog(msg, color = '#4ade80') {
        if (!logConsole) return;
        const span = document.createElement('div');
        span.style.color = color;
        span.style.padding = '2px 0';
        span.innerHTML = `<span style="opacity:0.5; margin-right:8px;">[${new Date().toLocaleTimeString()}]</span> ${msg}`;
        logConsole.appendChild(span);
        logConsole.scrollTop = logConsole.scrollHeight;
    }

    function updateProgress(val, statusText) {
        if (progressBar) progressBar.style.width = `${val}%`;
        if (progressText) progressText.innerText = `${val}%`;
        if (statusText) {
            if (progressDetail) progressDetail.innerText = statusText.toUpperCase();
            addLog(statusText, '#bc13fe');
        }
    }

    function resetLayers() {
        document.querySelectorAll('.layer-item').forEach(item => {
            const status = item.querySelector('.l-status');
            if (status) {
                status.innerText = 'IDLE';
                status.className = 'l-status status-idle';
            }
        });
    }

    async function fetchReports() {
        if (!reportList) return;
        try {
            const response = await fetch('/api/reports');
            const files = await response.json();
            reportList.innerHTML = '';
            files.forEach(f => {
                const li = document.createElement('li');
                li.innerHTML = `
                    <div class="item-info">
                        <span class="item-name" title="${f.name}">${f.name.split('.')[0]}</span>
                        <small style="color:var(--text-dim); font-size:0.65rem;">${new Date(f.time * 1000).toLocaleString()}</small>
                    </div>
                    <a href="/reports/${f.name}" target="_blank">OPEN REPORT</a>
                `;
                reportList.appendChild(li);
            });
        } catch (e) { console.error("Fetch reports failed", e); }
    }

    async function fetchPayloads() {
        if (!payloadList) return;
        try {
            const response = await fetch('/api/payloads');
            const tree = await response.json();
            payloadList.innerHTML = '';
            tree.forEach(t => {
                const li = document.createElement('li');
                li.innerHTML = `
                    <div class="item-info">
                       <span class="item-name" title="${t.target}">📦 Targets: ${t.target}</span>
                       <small style="color:var(--neon-cyan);">${t.files.length} payloads generated</small>
                    </div>
                    <div class="repo-meta-icon">⚙️</div>
                `;
                payloadList.appendChild(li);
            });
        } catch (e) { console.error("Fetch payloads failed", e); }
    }
});
