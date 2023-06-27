document.addEventListener("DOMContentLoaded", function() {
        var dashboardTab = document.getElementById("dashboard-tab");
        var mainContent = document.getElementById("main-content");

        dashboardTab.addEventListener("click", function(event) {
            event.preventDefault();
            mainContent.classList.toggle("active");

            // Get the username of the logged-in user (Ensure to replace this logic with API from the server side)
            var username = "John Doe";

            // Create a greeting message element
            var greetingElement = document.createElement("h2");
            greetingElement.textContent = "Hello! " + username;

            // Clear the existing content
            mainContent.innerHTML = "";

            // Append the greeting message to the main content
            mainContent.appendChild(greetingElement);

        });

        var appointmentsTab = document.getElementById("appointments-tab");
        var appointmentContent = document.getElementById("appointment-content");
        var appointmentHistoryBtn = document.getElementById("appointment-history-btn");
        var scheduleAppointmentBtn = document.getElementById("schedule-appointment-btn");
        var scheduleAppointmentForm = document.getElementById("schedule-appointment-form");
        var appointmentHistoryContainer = document.getElementById("appointmentHistoryContainer");
        var scheduledAppointments = [];


        appointmentsTab.addEventListener("click", function(event) {
            event.preventDefault();
            appointmentContent.classList.toggle("active");
        });

        scheduleAppointmentBtn.addEventListener("click", function(event) {
            event.preventDefault();
            scheduleAppointmentForm.style.display = "block";

            // Clear the content of the form
            scheduleAppointmentForm.reset();

            // Hide the appointment history details
            appointmentHistoryContainer.innerHTML = "";

            // Show the schedule appointment form
            scheduleAppointmentForm.style.display = "block";
        });

        scheduleAppointmentForm.addEventListener("submit", function(event) {
            event.preventDefault();

            // Get the values from the form inputs
            var appointmentDate = document.getElementById("appointment-date").value;
            var selectedDoctor = document.getElementById("doctor-select").value;
            var symptoms = document.getElementById("symptoms").value;

            // Validate the form inputs (add more validation logic)
            if (appointmentDate === "" || selectedDoctor === "" || symptoms === "") {
                alert("Please fill in all fields before submitting the form.");
                return;
            }

            // Check if the same appointment details already exist in the appointment history
            var isDuplicate = scheduledAppointments.some(function(appointment) {
                return (
                    !appointment.canceled &&
                    appointment.date === appointmentDate &&
                    appointment.doctor === selectedDoctor &&
                    appointment.symptoms === symptoms
                );
            });

            if (isDuplicate) {
                alert("This appointment is already scheduled.");
                return;
            }

            // Create an object with the appointment details
            var appointment = {
                date: appointmentDate,
                doctor: selectedDoctor,
                symptoms: symptoms,
                canceled: false // Initialize the "canceled" property to false
            };

            // Add the appointment object to the scheduledAppointments array
            scheduledAppointments.push(appointment);


            // Update the displayed appointments in Appointment History
            displayScheduledAppointments();

        });

        function displayScheduledAppointments() {
            // Hide the schedule appointment form
            scheduleAppointmentForm.style.display = "none";

            // Clear the existing content of the appointment history container
            appointmentHistoryContainer.innerHTML = "";

            // Create an unordered list element to display the appointments
            var appointmentList = document.createElement("ul");

            // Iterate over the scheduledAppointments array and create list items for each appointment
            scheduledAppointments.forEach(function(appointment) {
                if (!appointment.canceled) {
                    var listItem = document.createElement("li");
                    var appointmentDetails = document.createElement("div");
                    appointmentDetails.textContent =
                        "Date: " +
                        appointment.date +
                        ", Doctor: " +
                        appointment.doctor +
                        ", Symptoms: " +
                        appointment.symptoms;
                    listItem.appendChild(appointmentDetails);

                    // Add a "Cancel Appointment" button for each appointment
                    var cancelButton = document.createElement("button");
                    cancelButton.textContent = "Cancel Appointment";
                    cancelButton.addEventListener("click", function () {
                        // Set the "canceled" property to true
                        appointment.canceled = true;
                        // Update the displayed appointments in Appointment History
                        displayScheduledAppointments();
                    });
                    listItem.appendChild(cancelButton);

                    appointmentList.appendChild(listItem);
                }
            });

            // Append the appointment list to the appointment history container
            appointmentHistoryContainer.appendChild(appointmentList);
        }

            appointmentHistoryBtn.addEventListener("click", function(event) {
                     event.preventDefault();
                 displayScheduledAppointments();

        });



        appointmentContent.addEventListener("transitionend", function() {
            if (appointmentContent.classList.contains("active")) {
                appointmentHistoryBtn.style.display = "inline-block";
                scheduleAppointmentBtn.style.display = "inline-block";
            } else {
                appointmentHistoryBtn.style.display = "none";
                scheduleAppointmentBtn.style.display = "none";
            }
        });

        var profileSettings = document.getElementById("profile-settings");
        var dropdownContent = document.getElementById("dropdown-content");
        var profileForm = document.getElementById("profile-form");
        var passwordForm = document.getElementById("password-form");

        profileSettings.addEventListener("click", function(event) {
            event.preventDefault();
            dropdownContent.classList.toggle("active");
        });

        var editProfileLink = document.getElementById("edit-profile-link");
        var changePasswordLink = document.getElementById("change-password-link");

        editProfileLink.addEventListener("click", function(event) {
            event.preventDefault();
            profileForm.style.display = "block";
            passwordForm.style.display = "none";
        });

        changePasswordLink.addEventListener("click", function(event) {
            event.preventDefault();
            profileForm.style.display = "none";
            passwordForm.style.display = "block";
        });

        // Event handler for the profile form submit
        profileForm.addEventListener("submit", function(event) {
            event.preventDefault();
            // Retrieve the form values
            var name = document.getElementById("name").value;
            var email = document.getElementById("email").value;
            var address = document.getElementById("address").value;
            var phone = document.getElementById("phone").value;

            // Add your logic to handle the profile form submission
            // For example, you can send the form values to the server for updating the user profile
            console.log("Profile Form Submitted");
            console.log("Name: " + name);
            console.log("Email: " + email);
            console.log("Address: " + address);
            console.log("Phone: " + phone);
        });

        // Event handler for the password form submit
        passwordForm.addEventListener("submit", function(event) {
            event.preventDefault();
            // Retrieve the form values
            var oldPassword = document.getElementById("old-password").value;
            var newPassword = document.getElementById("new-password").value;
            var confirmPassword = document.getElementById("confirm-password").value;

            // Add your logic to handle the password form submission
            // For example, you can validate the old and new passwords, and update the password if valid
            console.log("Profile Form Submitted");
            console.log("Name: " + name);
            console.log("Email: " + email);
            console.log("Address: " + address);
            console.log("Phone: " + phone);
        });

        // Event handler for the password form submit
        passwordForm.addEventListener("submit", function(event) {
            event.preventDefault();
            // Retrieve the form values
            var oldPassword = document.getElementById("old-password").value;
            var newPassword = document.getElementById("new-password").value;
            var confirmPassword = document.getElementById("confirm-password").value;

            // Add your logic to handle the password form submission
            // For example, you can validate the old and new passwords, and update the password if valid
            console.log("Password Form Submitted");
            console.log("Old Password: " + oldPassword);
            console.log("New Password: " + newPassword);
            console.log("Confirm Password: " + confirmPassword);
        });

});



