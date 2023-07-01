document.addEventListener('DOMContentLoaded', function() {
    var dashboardButton = document.getElementById('dashboard-button');
    var doctorsButton = document.getElementById('doctors-button');
    var appointmentsButton = document.getElementById('appointments-button');
    var medicalRecordsButton = document.getElementById('medical-records-button');
    var profileSettingsButton = document.getElementById('profile-settings-button');
    var logoutSidebarButton = document.getElementById('logout-sidebar-button');

    dashboardButton.addEventListener('click', function() {
        // Implement functionality to load and display dashboard content
        console.log('Dashboard button clicked');
    });

    doctorsButton.addEventListener('click', function() {
        // Implement functionality to load and display doctors content
        console.log('Doctors button clicked');
    });

    appointmentsButton.addEventListener('click', function() {
        // Implement functionality to load and display appointments content
        console.log('Appointments button clicked');
    });

    medicalRecordsButton.addEventListener('click', function() {
        // Implement functionality to load and display medical records content
        console.log('Medical Records button clicked');
    });

    profileSettingsButton.addEventListener('click', function() {
        // Implement functionality to load and display profile settings content
        console.log('Profile Settings button clicked');
    });

    logoutSidebarButton.addEventListener('click', function() {
        // Implement functionality to logout the user
        console.log('Logout button clicked');
    });
});

