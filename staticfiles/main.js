// Enhanced Dummy Data with more realistic hospital data
const dummy = {
    patients: [
        { id: 1, name: 'Alice Smith', age: 29, gender: 'Female', diagnosis: 'Flu', admitted: '2024-06-01', status: 'Active' },
        { id: 2, name: 'Bob Johnson', age: 45, gender: 'Male', diagnosis: 'Diabetes', admitted: '2024-05-28', status: 'Active' },
        { id: 3, name: 'Carol White', age: 34, gender: 'Female', diagnosis: 'Asthma', admitted: '2024-06-02', status: 'Discharged' },
        { id: 4, name: 'David Brown', age: 52, gender: 'Male', diagnosis: 'Hypertension', admitted: '2024-06-03', status: 'Active' },
        { id: 5, name: 'Emma Davis', age: 38, gender: 'Female', diagnosis: 'Migraine', admitted: '2024-06-04', status: 'Active' },
    ],
    doctors: [
        { id: 1, name: 'Dr. John Doe', specialty: 'Cardiology', phone: '555-1234', email: 'john@hospital.com', patients: 12 },
        { id: 2, name: 'Dr. Jane Smith', specialty: 'Neurology', phone: '555-5678', email: 'jane@hospital.com', patients: 8 },
        { id: 3, name: 'Dr. Mike Wilson', specialty: 'Orthopedics', phone: '555-9012', email: 'mike@hospital.com', patients: 15 },
        { id: 4, name: 'Dr. Sarah Johnson', specialty: 'Pediatrics', phone: '555-3456', email: 'sarah@hospital.com', patients: 20 },
    ],
    appointments: [
        { id: 1, patient: 'Alice Smith', doctor: 'Dr. John Doe', date: '2024-06-10', time: '10:00', status: 'Scheduled' },
        { id: 2, patient: 'Bob Johnson', doctor: 'Dr. Jane Smith', date: '2024-06-11', time: '14:00', status: 'Completed' },
        { id: 3, patient: 'Carol White', doctor: 'Dr. Mike Wilson', date: '2024-06-12', time: '09:30', status: 'Scheduled' },
        { id: 4, patient: 'David Brown', doctor: 'Dr. Sarah Johnson', date: '2024-06-13', time: '16:00', status: 'Cancelled' },
    ],
    bills: [
        { id: 1, patient: 'Alice Smith', amount: 200, status: 'Paid', date: '2024-06-03' },
        { id: 2, patient: 'Bob Johnson', amount: 350, status: 'Unpaid', date: '2024-06-04' },
        { id: 3, patient: 'Carol White', amount: 180, status: 'Paid', date: '2024-06-05' },
        { id: 4, patient: 'David Brown', amount: 420, status: 'Unpaid', date: '2024-06-06' },
    ],
    reports: [
        { id: 1, title: 'Monthly Admissions', date: '2024-06-01', summary: '20 new admissions in June.', type: 'monthly' },
        { id: 2, title: 'Revenue Report', date: '2024-06-01', summary: 'Total revenue: $15,000.', type: 'revenue' },
        { id: 3, title: 'Patient Satisfaction', date: '2024-06-01', summary: '95% satisfaction rate.', type: 'monthly' },
        { id: 4, title: 'Department Performance', date: '2024-06-01', summary: 'All departments meeting targets.', type: 'revenue' },
    ],
    stats: {
        totalPatients: 156,
        activePatients: 89,
        totalDoctors: 24,
        totalRevenue: 125000,
        monthlyGrowth: 12.5
    }
};

// Enhanced Sidebar Logic with smooth animations
const sidebar = document.getElementById('sidebar');
const sidebarToggle = document.getElementById('sidebarToggle');
const mobileSidebarToggle = document.getElementById('mobileSidebarToggle');
const sidebarNavItems = document.querySelectorAll('.sidebar-nav li');

sidebarToggle.addEventListener('click', () => {
    sidebar.classList.toggle('closed');
    // Add animation class
    sidebar.style.animation = 'none';
    setTimeout(() => {
        sidebar.style.animation = 'slideInLeft 0.6s ease-out';
    }, 10);
});

mobileSidebarToggle.addEventListener('click', () => {
    sidebar.classList.toggle('open');
});

sidebarNavItems.forEach(item => {
    item.addEventListener('click', () => {
        // Remove active class from all items
        document.querySelector('.sidebar-nav li.active').classList.remove('active');
        item.classList.add('active');
        
        // Show loader with enhanced animation
        showLoader();
        
        // Simulate loading time for better UX
        setTimeout(() => {
            loadSection(item.getAttribute('data-section'));
            hideLoader();
            if (window.innerWidth < 900) sidebar.classList.remove('open');
        }, 800);
    });
});

// Enhanced Loader with better animations
const loader = document.getElementById('loader');
function showLoader() {
    loader.classList.remove('hidden');
    // Add entrance animation
    loader.style.animation = 'fadeIn 0.3s ease-out';
}

function hideLoader() {
    loader.style.animation = 'fadeOut 0.3s ease-out';
    setTimeout(() => {
        loader.classList.add('hidden');
    }, 300);
}

// Enhanced Section Content Loader with animations
const content = document.getElementById('content');
function loadSection(section) {
    // Add exit animation
    content.style.animation = 'fadeOutUp 0.3s ease-out';
    
    setTimeout(() => {
        switch(section) {
            case 'dashboard':
                renderDashboard(); break;
            case 'patients':
                renderPatients(); break;
            case 'appointments':
                renderAppointments(); break;
            case 'doctors':
                renderDoctors(); break;
            case 'billing':
                renderBilling(); break;
            case 'reports':
                renderReports(); break;
            case 'settings':
                renderSettings(); break;
            default:
                renderDashboard();
        }
        
        // Add entrance animation
        content.style.animation = 'fadeInUp 0.6s ease-out';
    }, 300);
}

// Initial load with animation
setTimeout(() => {
    loadSection('dashboard');
}, 500);

// Enhanced Dashboard with animated statistics
function renderDashboard() {
    content.innerHTML = `
        <h2><i class="fa fa-chart-line"></i> Dashboard</h2>
        <div class="dashboard-cards">
            <div class="card" data-count="${dummy.stats.totalPatients}">
                <i class="fa fa-user-injured"></i>
                <div>
                    <span class="counter">0</span>
                    <p>Total Patients</p>
                </div>
            </div>
            <div class="card" data-count="${dummy.stats.activePatients}">
                <i class="fa fa-user-md"></i>
                <div>
                    <span class="counter">0</span>
                    <p>Active Patients</p>
                </div>
            </div>
            <div class="card" data-count="${dummy.stats.totalDoctors}">
                <i class="fa fa-calendar-check"></i>
                <div>
                    <span class="counter">0</span>
                    <p>Doctors</p>
                </div>
            </div>
            <div class="card" data-count="${dummy.stats.totalRevenue}">
                <i class="fa fa-dollar-sign"></i>
                <div>
                    <span class="counter">0</span>
                    <p>Revenue ($)</p>
                </div>
            </div>
        </div>
        <div class="dashboard-stats">
            <div class="stat-item">
                <h3>Monthly Growth</h3>
                <div class="growth-indicator">
                    <span class="growth-value">+${dummy.stats.monthlyGrowth}%</span>
                    <i class="fa fa-arrow-up"></i>
                </div>
            </div>
        </div>
        <div class="dashboard-quick">
            <h3><i class="fa fa-chart-bar"></i> Recent Reports</h3>
            <ul>
                ${dummy.reports.slice(0, 3).map(r => `
                    <li class="report-item">
                        <i class='fa fa-file-medical-alt'></i>
                        <div>
                            <b>${r.title}</b>
                            <p>${r.summary}</p>
                        </div>
                    </li>
                `).join('')}
            </ul>
        </div>
    `;
    
    // Animate counters
    animateCounters();
}

// Animate number counters
function animateCounters() {
    const counters = document.querySelectorAll('.counter');
    counters.forEach(counter => {
        const target = parseInt(counter.parentElement.parentElement.dataset.count);
        const increment = target / 50;
        let current = 0;
        
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            counter.textContent = Math.floor(current).toLocaleString();
        }, 30);
    });
}

// Enhanced Patients Section
function renderPatients() {
    content.innerHTML = `
        <div class="section-header">
            <h2><i class="fa fa-user-injured"></i> Patient Records</h2>
            <button class="btn" onclick="openPatientModal()">
                <i class="fa fa-plus"></i> Add Patient
            </button>
        </div>
        <div class="table-responsive">
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Age</th>
                        <th>Gender</th>
                        <th>Diagnosis</th>
                        <th>Status</th>
                        <th>Admitted</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    ${dummy.patients.map(p => `
                        <tr class="table-row">
                            <td data-label="Name">${p.name}</td>
                            <td data-label="Age">${p.age}</td>
                            <td data-label="Gender">${p.gender}</td>
                            <td data-label="Diagnosis">${p.diagnosis}</td>
                            <td data-label="Status">
                                <span class="status-badge ${p.status.toLowerCase()}">${p.status}</span>
                            </td>
                            <td data-label="Admitted">${p.admitted}</td>
                            <td data-label="Actions">
                                <button class="btn btn-sm" onclick="editPatient(${p.id})">
                                    <i class="fa fa-edit"></i>
                                </button>
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        </div>
    `;
    
    // Add row entrance animations
    animateTableRows();
}

// Enhanced Appointments Section
function renderAppointments() {
    content.innerHTML = `
        <div class="section-header">
            <h2><i class="fa fa-calendar-check"></i> Appointment Scheduling</h2>
            <button class="btn" onclick="openAppointmentModal()">
                <i class="fa fa-plus"></i> Add Appointment
            </button>
        </div>
        <div class="table-responsive">
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Patient</th>
                        <th>Doctor</th>
                        <th>Date</th>
                        <th>Time</th>
                        <th>Status</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    ${dummy.appointments.map(a => `
                        <tr class="table-row">
                            <td data-label="Patient">${a.patient}</td>
                            <td data-label="Doctor">${a.doctor}</td>
                            <td data-label="Date">${a.date}</td>
                            <td data-label="Time">${a.time}</td>
                            <td data-label="Status">
                                <span class="status-badge ${a.status.toLowerCase()}">${a.status}</span>
                            </td>
                            <td data-label="Actions">
                                <button class="btn btn-sm" onclick="editAppointment(${a.id})">
                                    <i class="fa fa-edit"></i>
                                </button>
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        </div>
    `;
    
    animateTableRows();
}

// Enhanced Doctors Section
function renderDoctors() {
    content.innerHTML = `
        <div class="section-header">
            <h2><i class="fa fa-user-md"></i> Doctor Management</h2>
            <button class="btn" onclick="openDoctorModal()">
                <i class="fa fa-plus"></i> Add Doctor
            </button>
        </div>
        <div class="table-responsive">
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Specialty</th>
                        <th>Phone</th>
                        <th>Email</th>
                        <th>Patients</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    ${dummy.doctors.map(d => `
                        <tr class="table-row">
                            <td data-label="Name">${d.name}</td>
                            <td data-label="Specialty">${d.specialty}</td>
                            <td data-label="Phone">${d.phone}</td>
                            <td data-label="Email">${d.email}</td>
                            <td data-label="Patients">${d.patients}</td>
                            <td data-label="Actions">
                                <button class="btn btn-sm" onclick="editDoctor(${d.id})">
                                    <i class="fa fa-edit"></i>
                                </button>
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        </div>
    `;
    
    animateTableRows();
}

// Enhanced Billing Section
function renderBilling() {
    content.innerHTML = `
        <div class="section-header">
            <h2><i class="fa fa-file-invoice-dollar"></i> Billing</h2>
            <button class="btn" onclick="openBillModal()">
                <i class="fa fa-plus"></i> Add Bill
            </button>
        </div>
        <div class="table-responsive">
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Patient</th>
                        <th>Amount</th>
                        <th>Status</th>
                        <th>Date</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    ${dummy.bills.map(b => `
                        <tr class="table-row">
                            <td data-label="Patient">${b.patient}</td>
                            <td data-label="Amount">$${b.amount}</td>
                            <td data-label="Status">
                                <span class="status-badge ${b.status.toLowerCase()}">${b.status}</span>
                            </td>
                            <td data-label="Date">${b.date}</td>
                            <td data-label="Actions">
                                <button class="btn btn-sm" onclick="editBill(${b.id})">
                                    <i class="fa fa-edit"></i>
                                </button>
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        </div>
    `;
    
    animateTableRows();
}

// Enhanced Reports Section with tabs
function renderReports() {
    content.innerHTML = `
        <h2><i class="fa fa-file-medical-alt"></i> Reports</h2>
        <div class="tabs">
            <div class="tab active" data-tab="monthly">Monthly Reports</div>
            <div class="tab" data-tab="revenue">Revenue Reports</div>
            <div class="tab" data-tab="analytics">Analytics</div>
        </div>
        <div class="tab-content" id="reportTabContent"></div>
    `;
    
    const tabs = content.querySelectorAll('.tab');
    const tabContent = content.querySelector('#reportTabContent');
    
    function showTab(tab) {
        tabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        
        const tabType = tab.dataset.tab;
        let content = '';
        
        switch(tabType) {
            case 'monthly':
                content = `
                    <div class="report-grid">
                        ${dummy.reports.filter(r => r.type === 'monthly').map(r => `
                            <div class="report-card">
                                <h4>${r.title}</h4>
                                <p>${r.summary}</p>
                                <small>${r.date}</small>
                            </div>
                        `).join('')}
                    </div>
                `;
                break;
            case 'revenue':
                content = `
                    <div class="report-grid">
                        ${dummy.reports.filter(r => r.type === 'revenue').map(r => `
                            <div class="report-card">
                                <h4>${r.title}</h4>
                                <p>${r.summary}</p>
                                <small>${r.date}</small>
                            </div>
                        `).join('')}
                    </div>
                `;
                break;
            case 'analytics':
                content = `
                    <div class="analytics-dashboard">
                        <div class="chart-container">
                            <h3>Patient Growth</h3>
                            <div class="chart-placeholder">
                                <i class="fa fa-chart-line"></i>
                                <p>Interactive charts would be displayed here</p>
                            </div>
                        </div>
                    </div>
                `;
                break;
        }
        
        tabContent.innerHTML = content;
        animateReportCards();
    }
    
    tabs.forEach(tab => {
        tab.addEventListener('click', () => showTab(tab));
    });
    
    showTab(tabs[0]);
}

// Enhanced Settings Section
function renderSettings() {
    content.innerHTML = `
        <h2><i class="fa fa-cog"></i> Settings</h2>
        <div class="settings-grid">
            <div class="settings-card">
                <h3><i class="fa fa-palette"></i> Appearance</h3>
                <div class="setting-item">
                    <label>Theme:</label>
                    <button class="btn" id="settingsThemeToggle">
                        <i class="fa fa-moon"></i> Toggle Light/Dark
                    </button>
                </div>
            </div>
            <div class="settings-card">
                <h3><i class="fa fa-bell"></i> Notifications</h3>
                <div class="setting-item">
                    <label>
                        <input type="checkbox" checked> Enable notifications
                    </label>
                </div>
            </div>
            <div class="settings-card">
                <h3><i class="fa fa-user"></i> Profile</h3>
                <div class="setting-item">
                    <button class="btn">
                        <i class="fa fa-user"></i> Edit Profile
                    </button>
                </div>
            </div>
        </div>
    `;
    
    document.getElementById('settingsThemeToggle').onclick = () => toggleTheme();
}

// Enhanced Modal Functions
window.openPatientModal = function() {
    openModal(`
        <h3><i class="fa fa-user-plus"></i> Add Patient</h3>
        <form id='patientForm'>
            <input type='text' name='name' placeholder='Full Name' required>
            <input type='number' name='age' placeholder='Age' required>
            <select name='gender' required>
                <option value="">Select Gender</option>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
            </select>
            <input type='text' name='diagnosis' placeholder='Diagnosis' required>
            <input type='date' name='admitted' required>
            <select name='status' required>
                <option value="">Select Status</option>
                <option value="Active">Active</option>
                <option value="Discharged">Discharged</option>
            </select>
            <button type='submit' class='btn'>
                <i class='fa fa-save'></i> Save Patient
            </button>
        </form>
    `);
    
    setupFormSubmission('patientForm', (data) => {
        dummy.patients.push({
            id: Date.now(),
            ...data
        });
        renderPatients();
    });
};

// Enhanced Modal Logic
const modal = document.getElementById('modal');
const modalBody = document.getElementById('modalBody');
const closeModalBtn = document.getElementById('closeModal');

function openModal(html) {
    modalBody.innerHTML = html;
    modal.classList.remove('hidden');
    setTimeout(() => {
        modal.querySelector('.modal-content').style.transform = 'scale(1)';
    }, 10);
}

function closeModal() {
    modal.classList.add('hidden');
}

closeModalBtn.onclick = closeModal;
window.onclick = function(event) {
    if (event.target === modal) closeModal();
};

// Enhanced Light/Dark Mode Toggle
const themeToggle = document.getElementById('themeToggle');
function toggleTheme() {
    document.body.classList.toggle('dark');
    const icon = themeToggle.querySelector('i');
    icon.className = document.body.classList.contains('dark') ? 'fa fa-sun' : 'fa fa-moon';
    
    // Add transition effect
    document.body.style.transition = 'all 0.3s ease';
}

themeToggle.onclick = toggleTheme;

// Animation Functions
function animateTableRows() {
    const rows = document.querySelectorAll('.table-row');
    rows.forEach((row, index) => {
        row.style.opacity = '0';
        row.style.transform = 'translateX(-20px)';
        setTimeout(() => {
            row.style.transition = 'all 0.3s ease';
            row.style.opacity = '1';
            row.style.transform = 'translateX(0)';
        }, index * 100);
    });
}

function animateReportCards() {
    const cards = document.querySelectorAll('.report-card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        setTimeout(() => {
            card.style.transition = 'all 0.3s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 150);
    });
}

// Utility Functions
function setupFormSubmission(formId, callback) {
    const form = document.getElementById(formId);
    if (form) {
        form.onsubmit = function(e) {
            e.preventDefault();
            const formData = new FormData(form);
            const data = {};
            for (let [key, value] of formData.entries()) {
                data[key] = value;
            }
            closeModal();
            showLoader();
            setTimeout(() => {
                callback(data);
                hideLoader();
            }, 500);
        };
    }
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    @keyframes fadeOut { from { opacity: 1; } to { opacity: 0; } }
    @keyframes fadeOutUp { from { opacity: 1; transform: translateY(0); } to { opacity: 0; transform: translateY(-20px); } }
    
    .status-badge {
        padding: 0.3rem 0.8rem;
        border-radius: 1rem;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
    }
    
    .status-badge.active { background: rgba(72, 187, 120, 0.2); color: #48bb78; }
    .status-badge.discharged { background: rgba(66, 153, 225, 0.2); color: #4299e1; }
    .status-badge.scheduled { background: rgba(237, 137, 54, 0.2); color: #ed8936; }
    .status-badge.completed { background: rgba(72, 187, 120, 0.2); color: #48bb78; }
    .status-badge.cancelled { background: rgba(245, 101, 101, 0.2); color: #f56565; }
    .status-badge.paid { background: rgba(72, 187, 120, 0.2); color: #48bb78; }
    .status-badge.unpaid { background: rgba(245, 101, 101, 0.2); color: #f56565; }
    
    .dashboard-stats {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin-bottom: 2rem;
    }
    
    .stat-item {
        background: var(--bg-glass);
        padding: 1.5rem;
        border-radius: 1rem;
        backdrop-filter: blur(var(--blur));
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .growth-indicator {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: var(--success);
        font-weight: 600;
    }
    
    .report-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.5rem;
    }
    
    .report-card {
        background: var(--bg-glass);
        padding: 1.5rem;
        border-radius: 1rem;
        backdrop-filter: blur(var(--blur));
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
    }
    
    .report-card:hover {
        transform: translateY(-5px);
        box-shadow: var(--shadow-light);
    }
    
    .settings-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.5rem;
    }
    
    .settings-card {
        background: var(--bg-glass);
        padding: 1.5rem;
        border-radius: 1rem;
        backdrop-filter: blur(var(--blur));
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .setting-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 1rem;
    }
    
    .analytics-dashboard {
        background: var(--bg-glass);
        padding: 2rem;
        border-radius: 1rem;
        backdrop-filter: blur(var(--blur));
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .chart-placeholder {
        text-align: center;
        padding: 3rem;
        color: var(--text-light);
    }
    
    .chart-placeholder i {
        font-size: 3rem;
        margin-bottom: 1rem;
        color: var(--primary);
    }
    
    .report-item {
        display: flex;
        align-items: flex-start;
        gap: 1rem;
    }
    
    .report-item div {
        flex: 1;
    }
    
    .report-item p {
        margin: 0.5rem 0 0 0;
        color: var(--text-light);
        font-size: 0.9rem;
    }
`;
document.head.appendChild(style); 