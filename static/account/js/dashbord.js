 // Automatically show the modal when the page loads


 document.addEventListener('DOMContentLoaded', function () {
    
    const modalContainer = document.getElementById('modal');
    const modalHeaderBtn = document.getElementById('modl-header-btn');
    const modalFootBtn = document.getElementById('modl-foot-btn');

    if (modalContainer && modalHeaderBtn && modalFootBtn) {

        // Function to close modal smoothly
        function closeModal() {
            if (modalContainer) {
                // console.log('hidden code  works')
                modalContainer.classList.add('hidden'); // Add hidden class to trigger smooth close
            }
        }

        // Close modal when header button is clicked
        modalHeaderBtn.addEventListener('click', closeModal);

        // Close modal when footer button is clicked
        modalFootBtn.addEventListener('click', closeModal);
    }
})



// GRAPH CODE START

const years = JSON.parse(document.getElementById('years').innerText);
const patient_growth = JSON.parse(document.getElementById('growth').innerText);

// console.log("years:", years);
// console.log("growth:", patient_growth);

// Create the chart

const barCtx = document.getElementById('patientGrowthChart').getContext('2d'); // Renamed to barCtx

// Create gradient for the bars
const gradient =barCtx.createLinearGradient(0, 0, 0, 400);
gradient.addColorStop(0, 'rgba(54, 162, 235, 1)'); // Top color
gradient.addColorStop(1, 'rgba(54, 162, 235, 0.2)'); // Bottom color

// Simulated 3D Bar Chart
const patientGrowthChart = new Chart(barCtx, {

    type: 'bar',
    data: {
        labels: years,
        datasets: [{
            label: 'Yearly Patient Growth',
            data: patient_growth,
            backgroundColor: gradient,
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1,
            borderSkipped: false, // Removes the flat top to mimic 3D
            barThickness: 20, // Thickness of bars
            hoverBackgroundColor: 'rgba(54, 162, 235, 0.8)', // Hover effect
        }]
    },
    options: {
        plugins: {
            legend: {
                display: true, // Show legend
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                grid: {
                    drawBorder: true,
                    color: 'rgba(200, 200, 200, 0.2)',
                }
            },
            x: {
                grid: {
                    display: false
                }
            }
        },
        elements: {
            bar: {
                borderWidth: 2,
            }
        }
    }
});


//PIR CHART CODE START

const department = document.getElementById('department').innerText;
const patient_count = document.getElementById('patient_count').innerText;

// Convert department string into an array
const departmentArray = department.replace(/[\[\]']+/g, '').split(',').map(item => item.trim());

// Convert patient count string into an array of integers
const patientCountArray = patient_count.split(',').map(item => {
    const parsedValue = parseInt(item.trim(), 10);
    if (isNaN(parsedValue)) {
        console.log(`Invalid value: ${item}`);  // Check which value is invalid
        return 0;  // Handle invalid value, or set a default value
    }
    return parsedValue;
});

const pieCtx = document.getElementById('departmentChart').getContext('2d');

// Calculate the total patient count
const totalPatients = patientCountArray.reduce((sum, val) => sum + val, 0);

const chart = new Chart(pieCtx, {
    type: 'pie',
    data: {
        labels: departmentArray,
        datasets: [{
            data: patientCountArray,
            backgroundColor: [
                '#FF6384', '#36A2EB', '#FFCE56', '#EB5B00', '#9966FF', '#4BC0C0'
            ],
            hoverOffset: 4
        }]
    },
    options: {
        plugins: {
            legend: {
                position: 'right',
                labels: {
                    boxWidth: 30,
                    padding: 5,
                    font: {
                        size:8.7,
                        weight: 'bold',
                        family: 'Arial, sans-serif',  // Specify the font family here
                    },
                    // Add percentage to legend labels
                    generateLabels: function(chart) {
                        const data = chart.data;
                        return data.labels.map(function(label, i) {
                            const percentage = ((data.datasets[0].data[i] / totalPatients) * 100).toFixed(1) + '%';
                            return {
                                text: `${label} (${percentage})`,  // Append percentage to the label
                                fillStyle: data.datasets[0].backgroundColor[i],
                                strokeStyle: data.datasets[0].backgroundColor[i],
                                lineWidth: 1
                            };
                        });
                    }
                }
            },
            title: {
                display: true,
                text: 'Patient Distribution (2023-2024)',
                font: {
                    size: 16,
                    weight: 'bold',
                },
                color: 'black',
                position: 'top',
                padding: {
                    top: 10,
                    bottom: 20
                }
            },
            tooltip: {
                callbacks: {
                    label: function(tooltipItem) {
                        const value = tooltipItem.raw;
                        const percentage = ((value / totalPatients) * 100).toFixed(1) + '%';
                        return tooltipItem.label + ': ' + percentage;
                    }
                }
            }
        }
    },
    plugins: []  // Completely remove ChartDataLabels plugin to avoid any label inside the slice
});


// PIE CODE END


//AVG CHART CODE START 

const departments = JSON.parse(document.getElementById('departments-data').textContent);
const ages = JSON.parse(document.getElementById('ages-data').textContent);


console.log('Departments:', departments);
console.log('Ages:', ages);

// Create gradient for the bars


const ctx = document.getElementById('avgAgeChart').getContext('2d');
const avgAgeChart = new Chart(ctx, {
    type: 'bar',
    data: {
        
        labels:departments,
        datasets: [{
            label: 'Average Patient Age',
            data:ages,
            // backgroundColor: 'rgba(68, 197, 197, 0.69)', // Bar color
            backgroundColor: gradient, // Bar color
            borderColor: 'rgba(54, 162, 235, 1)', // Border color
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        indexAxis: 'y', // This makes the chart horizontal
        plugins: {
            legend: {
                display: true
            }
        },
        scales: {
            x: {
                beginAtZero: true, // Ensures the X-axis starts at 0
            },
            y: {
                ticks: {
                    color:'black',
                    font: {
                        size: 10,
                        weight:'700'
                    }
                }
            }
        }
    }
});
//AVG CHART CODE END


//LINE CHART CODE START

 // Utility function for generating month labels (for example purposes)

 const months = JSON.parse(document.getElementById('months').textContent);
 const counts = JSON.parse(document.getElementById('counts').textContent);

 console.log('months: ',months)
 console.log('counts: ',counts)


//  const Utils = {
//     months: function ({ count }) {
//       const monthNames = ['January', 'February', 'March', 'April', 'May', 'June', 'July'];
//       return monthNames.slice(0, count);
//     }
//   };

  // Define labels and data
//   const labels = Utils.months({ count: 7 });

  const data = {
    labels: months,
    datasets: [{
      label: 'Patient data per month',
      data:counts ,
      fill: false,
      borderColor: 'rgb(75, 192, 192)',
      tension: 0.1
    }]
  };

  // Config and render the chart
  const config = {
    type: 'line', // You can change this to 'bar', 'pie', etc.
    data: data,
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'top',
        },
        title: {
          display: true,
          text: 'Sample Chart'
        }
      }
    }
  };

  // Render the chart
  const myChart = new Chart(
    document.getElementById('linechartId'),
    config
  );

//LINE SHART CODE END

// GRAPH CODE END