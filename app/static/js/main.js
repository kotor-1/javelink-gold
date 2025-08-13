// Javelink Lite Frontend JavaScript

let analysisResult = null;

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('uploadForm');
    const submitBtn = document.getElementById('submitBtn');
    const progressContainer = document.getElementById('progressContainer');
    const resultsContainer = document.getElementById('resultsContainer');
    const errorContainer = document.getElementById('errorContainer');
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Get form data
        const formData = new FormData();
        const fileInput = document.getElementById('videoFile');
        const view = document.querySelector('input[name="view"]:checked').value;
        const handedness = document.getElementById('handedness').value;
        const scaleMethod = document.getElementById('scaleMethod').value;
        
        formData.append('file', fileInput.files[0]);
        formData.append('view', view);
        formData.append('handedness', handedness);
        formData.append('scale_method', scaleMethod);
        
        // UI state
        submitBtn.disabled = true;
        progressContainer.classList.remove('hidden');
        resultsContainer.classList.add('hidden');
        errorContainer.classList.add('hidden');
        
        try {
            // Send request
            const response = await fetch('/api/analyze', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            if (response.ok && !result.error) {
                analysisResult = result;
                displayResults(result);
                resultsContainer.classList.remove('hidden');
            } else {
                throw new Error(result.error || 'Analysis failed');
            }
        } catch (error) {
            console.error('Error:', error);
            document.getElementById('errorMessage').textContent = error.message;
            errorContainer.classList.remove('hidden');
        } finally {
            submitBtn.disabled = false;
            progressContainer.classList.add('hidden');
        }
    });
    
    // Download handlers
    document.getElementById('downloadVideo')?.addEventListener('click', () => {
        if (analysisResult?.annotated_video_path) {
            window.open(analysisResult.annotated_video_path, '_blank');
        }
    });
    
    document.getElementById('downloadJSON')?.addEventListener('click', () => {
        if (analysisResult) {
            const blob = new Blob([JSON.stringify(analysisResult, null, 2)], 
                                 {type: 'application/json'});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'javelink_results.json';
            a.click();
            URL.revokeObjectURL(url);
        }
    });
});

function displayResults(result) {
    const metricsGrid = document.getElementById('metricsGrid');
    metricsGrid.innerHTML = '';
    
    // Define metrics to display based on view
    const metricsToShow = result.meta.view === 'side' ? [
        {key: 'release_angle_deg', label: '繝ｪ繝ｪ繝ｼ繧ｹ隗・, unit: 'ﾂｰ'},
        {key: 'release_height_m', label: '繝ｪ繝ｪ繝ｼ繧ｹ鬮倥＆', unit: 'm'},
        {key: 'release_speed_mps', label: '繝ｪ繝ｪ繝ｼ繧ｹ騾溷ｺｦ', unit: 'm/s'},
        {key: 'plant_to_release_ms', label: '繝励Λ繝ｳ繝遺・繝ｪ繝ｪ繝ｼ繧ｹ', unit: 'ms'}
    ] : [
        {key: 'plant_foot_progression_deg', label: '繝励Λ繝ｳ繝郁ｶｳ騾ｲ陦瑚ｧ・, unit: 'ﾂｰ'},
        {key: 'shoulder_hip_separation_deg', label: '閧ｩ-閻ｰ蛻・屬隗・, unit: 'ﾂｰ'},
        {key: 'lane_alignment_error_cm', label: '襍ｰ霍ｯ謨ｴ蛻苓ｪ､蟾ｮ', unit: 'cm'}
    ];
    
    // Create metric cards
    metricsToShow.forEach(metric => {
        const value = result.metrics[metric.key];
        if (value !== null && value !== undefined) {
            const card = createMetricCard(
                metric.label,
                value.toFixed(metric.unit === 'ms' ? 0 : 1),
                metric.unit,
                result.qc.overall_status
            );
            metricsGrid.appendChild(card);
        }
    });
    
    // Add QC notes if any
    if (result.qc.notes && result.qc.notes.length > 0) {
        const notesDiv = document.createElement('div');
        notesDiv.className = 'col-span-full mt-4 p-4 bg-yellow-50 border border-yellow-200 rounded-lg';
        notesDiv.innerHTML = `
            <h3 class="font-semibold text-yellow-800 mb-2">豕ｨ險・</h3>
            <ul class="list-disc list-inside text-sm text-yellow-700">
                ${result.qc.notes.map(note => `<li>${note}</li>`).join('')}
            </ul>
        `;
        metricsGrid.appendChild(notesDiv);
    }
}

function createMetricCard(label, value, unit, qcStatus) {
    const card = document.createElement('div');
    card.className = 'metric-card';
    
    const badgeClass = qcStatus === 'GOOD' ? 'qc-good' : 
                       qcStatus === 'WARN' ? 'qc-warn' : 'qc-fail';
    
    card.innerHTML = `
        <div class="flex justify-between items-start">
            <div>
                <div class="metric-value">${value} ${unit}</div>
                <div class="metric-label">${label}</div>
            </div>
            <span class="qc-badge ${badgeClass}">${qcStatus}</span>
        </div>
    `;
    
    return card;
}
