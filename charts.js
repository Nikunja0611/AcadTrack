// dashboard.html Charts
function renderStudentCharts(unit_test, end_sem, lab_attendance, overall_attendance) {
    const marksCtx = document.getElementById('marksChart').getContext('2d');
    const marksChart = new Chart(marksCtx, {
        type: 'bar',
        data: {
            labels: ['Unit Test', 'End Sem', 'Lab'],
            datasets: [{
                label: 'Marks',
                data: [unit_test, end_sem, lab_attendance],
                backgroundColor: ['rgba(75, 192, 192, 0.2)', 
                                  'rgba(153, 102, 255, 0.2)', 
                                  'rgba(255, 159, 64, 0.2)'],
                borderColor: ['rgba(75, 192, 192, 1)', 
                              'rgba(153, 102, 255, 1)', 
                              'rgba(255, 159, 64, 1)'],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: { beginAtZero: true }
            }
        }
    });

    const attendanceCtx = document.getElementById('attendanceChart').getContext('2d');
    const attendanceChart = new Chart(attendanceCtx, {
        type: 'pie',
        data: {
            labels: ['Present', 'Absent'],
            datasets: [{
                label: 'Attendance',
                data: [overall_attendance, 100 - overall_attendance],
                backgroundColor: [
                    'rgba(54, 162, 235, 0.6)',
                    'rgba(255, 99, 132, 0.6)'
                ],
                borderColor: [
                    'rgba(54, 162, 235, 1)',
                    'rgba(255,99,132,1)'
                ],
                borderWidth: 1
            }]
        }
    });
}

// professor_dashboard.html Charts
function renderProfessorCharts(avg_unit_test, avg_end_sem, avg_overall_attendance) {
    const overallCtx = document.getElementById('overallChart').getContext('2d');
    const overallChart = new Chart(overallCtx, {
        type: 'bar',
        data: {
            labels: ['Average Unit Test', 'Average End Sem', 'Average Attendance'],
            datasets: [{
                label: 'Average Scores',
                data: [avg_unit_test, avg_end_sem, avg_overall_attendance],
                backgroundColor: ['rgba(255, 206, 86, 0.6)', 
                                  'rgba(75, 192, 192, 0.6)', 
                                  'rgba(153, 102, 255, 0.6)'],
                borderColor: ['rgba(255, 206, 86, 1)', 
                              'rgba(75, 192, 192, 1)', 
                              'rgba(153, 102, 255, 1)'],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
}
