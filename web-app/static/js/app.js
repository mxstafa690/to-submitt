/**
 * Main Application Logic
 * This file contains all the UI interaction logic
 */

// Wait for the page to load
document.addEventListener('DOMContentLoaded', function() {
    console.log('FitTrack app loaded!');
    
    // Initialize the app
    initializeApp();
});

/**
 * Initialize the application
 */
function initializeApp() {
    // Set up navigation
    setupNavigation();
    
    // Load initial data
    loadMembers();
    loadClasses();
    loadPlans();
    loadCheckins();
    
    // Set up form handlers
    setupMemberForm();
    setupClassForm();
    setupPlanForm();
}

/**
 * Set up navigation between sections
 */
function setupNavigation() {
    const navButtons = document.querySelectorAll('.nav-btn');
    
    navButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Get the section to show
            const sectionName = this.dataset.section;
            
            // Hide all sections
            document.querySelectorAll('.section').forEach(section => {
                section.classList.remove('active');
            });
            
            // Remove active class from all buttons
            navButtons.forEach(btn => btn.classList.remove('active'));
            
            // Show selected section
            document.getElementById(`${sectionName}-section`).classList.add('active');
            
            // Add active class to clicked button
            this.classList.add('active');
        });
    });
}

/**
 * Load and display members
 */
async function loadMembers() {
    const membersList = document.getElementById('members-list');
    
    try {
        const members = await api.getMembers();
        
        if (members.length === 0) {
            membersList.innerHTML = '<div class="loading">No members found. Add your first member!</div>';
            return;
        }
        
        // Clear loading message
        membersList.innerHTML = '';
        
        // Create cards for each member
        members.forEach(member => {
            const card = createMemberCard(member);
            membersList.appendChild(card);
        });
        
    } catch (error) {
        membersList.innerHTML = '<div class="error-message">Failed to load members. Make sure the backend is running on port 5000.</div>';
        console.error('Error loading members:', error);
    }
}

/**
 * Create a member card element
 */
function createMemberCard(member) {
    const card = document.createElement('div');
    card.className = 'card';
    
    const statusBadge = member.status === 'active' ? 'active' : 'inactive';
    
    card.innerHTML = `
        <h3>${member.full_name}</h3>
        <p><strong>Email:</strong> ${member.email}</p>
        <p><strong>Phone:</strong> ${member.phone}</p>
        <p><strong>National ID:</strong> ${member.national_id}</p>
        <p><strong>Member Since:</strong> ${formatDate(member.created_at)}</p>
        <span class="badge ${statusBadge}">${member.status}</span>
    `;
    
    return card;
}

/**
 * Load and display classes
 */
async function loadClasses() {
    const classesList = document.getElementById('classes-list');
    
    try {
        const classes = await api.getClasses();
        
        if (classes.length === 0) {
            classesList.innerHTML = '<div class="loading">No classes scheduled yet.</div>';
            return;
        }
        
        classesList.innerHTML = '';
        
        classes.forEach(gymClass => {
            const card = createClassCard(gymClass);
            classesList.appendChild(card);
        });
        
    } catch (error) {
        classesList.innerHTML = '<div class="error-message">Failed to load classes.</div>';
        console.error('Error loading classes:', error);
    }
}

/**
 * Create a class card element
 */
function createClassCard(gymClass) {
    const card = document.createElement('div');
    card.className = 'card';
    
    const startTime = formatDateTime(gymClass.start_time);
    const availableSlots = gymClass.stats ? gymClass.stats.available_slots : gymClass.capacity;
    const enrolled = gymClass.stats ? gymClass.stats.active_registrations : 0;
    
    card.innerHTML = `
        <h3>${gymClass.title}</h3>
        <p><strong>Instructor:</strong> ${gymClass.instructor}</p>
        <p><strong>Starts:</strong> ${startTime}</p>
        <p><strong>Duration:</strong> ${gymClass.duration_minutes} minutes</p>
        <p><strong>Capacity:</strong> ${enrolled}/${gymClass.capacity} enrolled</p>
        <p><strong>Available:</strong> ${availableSlots} spots</p>
    `;
    
    return card;
}

/**
 * Load and display membership plans
 */
async function loadPlans() {
    const plansList = document.getElementById('plans-list');
    
    try {
        const plans = await api.getPlans();
        
        if (plans.length === 0) {
            plansList.innerHTML = '<div class="loading">No plans available.</div>';
            return;
        }
        
        plansList.innerHTML = '';
        
        plans.forEach(plan => {
            const card = createPlanCard(plan);
            plansList.appendChild(card);
        });
        
    } catch (error) {
        plansList.innerHTML = '<div class="error-message">Failed to load plans.</div>';
        console.error('Error loading plans:', error);
    }
}

/**
 * Create a plan card element
 */
function createPlanCard(plan) {
    const card = document.createElement('div');
    card.className = 'card';
    
    const maxEntriesText = plan.max_entries ? `${plan.max_entries} visits` : 'Unlimited';
    
    card.innerHTML = `
        <h3>${plan.name}</h3>
        <p><strong>Type:</strong> ${plan.type}</p>
        <p><strong>Price:</strong> $${plan.price.toFixed(2)}</p>
        <p><strong>Valid for:</strong> ${plan.valid_days} days</p>
        <p><strong>Max Entries:</strong> ${maxEntriesText}</p>
    `;
    
    return card;
}

/**
 * Load and display check-ins
 */
async function loadCheckins() {
    const checkinsList = document.getElementById('checkins-list');
    
    try {
        const checkins = await api.getCheckins();
        
        if (checkins.length === 0) {
            checkinsList.innerHTML = '<div class="loading">No check-ins recorded yet.</div>';
            return;
        }
        
        checkinsList.innerHTML = '';
        
        // Show only the latest 20 check-ins
        checkins.slice(0, 20).forEach(checkin => {
            const item = createCheckinItem(checkin);
            checkinsList.appendChild(item);
        });
        
    } catch (error) {
        checkinsList.innerHTML = '<div class="error-message">Failed to load check-ins.</div>';
        console.error('Error loading check-ins:', error);
    }
}

/**
 * Create a check-in list item
 */
function createCheckinItem(checkin) {
    const item = document.createElement('div');
    item.className = 'list-item';
    
    item.innerHTML = `
        <div>
            <strong>Member ID: ${checkin.member_id}</strong>
            <p style="color: #666; font-size: 0.9rem;">${formatDateTime(checkin.checkin_time)}</p>
        </div>
        <span class="badge active">Checked In</span>
    `;
    
    return item;
}

/**
 * Show the add member form
 */
function showAddMemberForm() {
    document.getElementById('add-member-form').classList.remove('hidden');
}

/**
 * Hide the add member form
 */
function hideAddMemberForm() {
    document.getElementById('add-member-form').classList.add('hidden');
    document.getElementById('member-form').reset();
}

/**
 * Set up the member form submission
 */
function setupMemberForm() {
    const form = document.getElementById('member-form');
    
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Get form data
        const memberData = {
            full_name: document.getElementById('full-name').value,
            email: document.getElementById('email').value,
            phone: document.getElementById('phone').value,
            national_id: document.getElementById('national-id').value,
            password: document.getElementById('password').value
        };
        
        try {
            // Create the member
            await api.createMember(memberData);
            
            // Show success message
            showMessage('Member added successfully!', 'success');
            
            // Hide form and reload members
            hideAddMemberForm();
            loadMembers();
            
        } catch (error) {
            // Show the actual error message from the API
            let errorMessage = 'Failed to add member. ';
            
            if (error.message && error.message !== `HTTP error! status: ${error.status}`) {
                errorMessage += error.message;
            } else {
                errorMessage += 'Please check:\n';
                errorMessage += '• Email: valid format (e.g., user@example.com)\n';
                errorMessage += '• Phone: 10-15 digits (e.g., 050-1234567)\n';
                errorMessage += '• National ID: 9 digits (e.g., 123456789)\n';
                errorMessage += '• Password: 8+ chars with uppercase, lowercase, digit, and special character';
            }
            
            showMessage(errorMessage, 'error');
            console.error('Error creating member:', error);
        }
    });
}

/**
 * Show a message to the user
 */
function showMessage(message, type) {
    const messageDiv = document.createElement('div');
    messageDiv.className = type === 'success' ? 'success-message' : 'error-message';
    // Preserve line breaks in error messages
    messageDiv.style.whiteSpace = 'pre-line';
    messageDiv.textContent = message;
    
    const mainContent = document.querySelector('.main-content');
    mainContent.insertBefore(messageDiv, mainContent.firstChild);
    
    // Remove message after 5 seconds (longer for error messages)
    setTimeout(() => {
        messageDiv.remove();
    }, type === 'error' ? 8000 : 3000);
}

/**
 * Format a date string
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric' 
    });
}

/**
 * Format a date and time string
 */
function formatDateTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('en-US', { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Make functions available globally for onclick handlers
window.showAddMemberForm = showAddMemberForm;
window.hideAddMemberForm = hideAddMemberForm;
window.showAddClassForm = showAddClassForm;
window.hideAddClassForm = hideAddClassForm;
window.showAddPlanForm = showAddPlanForm;
window.hideAddPlanForm = hideAddPlanForm;

/**
 * Show the add class form
 */
function showAddClassForm() {
    document.getElementById('add-class-form').classList.remove('hidden');
}

/**
 * Hide the add class form
 */
function hideAddClassForm() {
    document.getElementById('add-class-form').classList.add('hidden');
    document.getElementById('class-form').reset();
}

/**
 * Set up the class form submission
 */
function setupClassForm() {
    const form = document.getElementById('class-form');
    
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Get form data
        const classData = {
            title: document.getElementById('class-title').value,
            instructor: document.getElementById('class-instructor').value,
            start_time: document.getElementById('class-start-time').value,
            duration_minutes: parseInt(document.getElementById('class-duration').value),
            capacity: parseInt(document.getElementById('class-capacity').value)
        };
        
        try {
            // Create the class
            await api.createClass(classData);
            
            // Show success message
            showMessage('Class added successfully!', 'success');
            
            // Hide form and reload classes
            hideAddClassForm();
            loadClasses();
            
        } catch (error) {
            let errorMessage = 'Failed to add class. ';
            if (error.message && error.message !== `HTTP error! status: ${error.status}`) {
                errorMessage += error.message;
            } else {
                errorMessage += 'Please check all fields: title (2-120 chars), instructor (2-120 chars), valid date/time, duration (15-300 min), capacity (1-300).';
            }
            showMessage(errorMessage, 'error');
            console.error('Error creating class:', error);
        }
    });
}

/**
 * Show the add plan form
 */
function showAddPlanForm() {
    document.getElementById('add-plan-form').classList.remove('hidden');
}

/**
 * Hide the add plan form
 */
function hideAddPlanForm() {
    document.getElementById('add-plan-form').classList.add('hidden');
    document.getElementById('plan-form').reset();
}

/**
 * Set up the plan form submission
 */
function setupPlanForm() {
    const form = document.getElementById('plan-form');
    
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Get form data
        const planData = {
            name: document.getElementById('plan-name').value,
            type: document.getElementById('plan-type').value,
            price: parseFloat(document.getElementById('plan-price').value),
            valid_days: parseInt(document.getElementById('plan-valid-days').value)
        };
        
        // Add max_entries only if provided
        const maxEntries = document.getElementById('plan-max-entries').value;
        if (maxEntries && maxEntries.trim() !== '') {
            planData.max_entries = parseInt(maxEntries);
        }
        
        try {
            // Create the plan
            await api.createPlan(planData);
            
            // Show success message
            showMessage('Plan added successfully!', 'success');
            
            // Hide form and reload plans
            hideAddPlanForm();
            loadPlans();
            
        } catch (error) {
            let errorMessage = 'Failed to add plan. ';
            if (error.message && error.message !== `HTTP error! status: ${error.status}`) {
                errorMessage += error.message;
            } else {
                errorMessage += 'Please check: name (2+ chars), type (3-30 chars), price (> 0), valid_days (> 0), max_entries (> 0 or empty).';
            }
            showMessage(errorMessage, 'error');
            console.error('Error creating plan:', error);
        }
    });
}
window.hideAddClassForm = hideAddClassForm;
window.showAddPlanForm = showAddPlanForm;
window.hideAddPlanForm = hideAddPlanForm;
window.hideAddMemberForm = hideAddMemberForm;
