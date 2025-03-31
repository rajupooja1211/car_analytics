import { Bar, Line } from "react-chartjs-2";
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, LineElement, PointElement } from "chart.js";

ChartJS.register(CategoryScale, LinearScale, BarElement, LineElement, PointElement);

export default function Charts({ analytics }) {
  const salesData = {
    labels: Object.keys(analytics.sales_by_company || {}),
    datasets: [
      {
        label: "Sales by Company",
        data: Object.values(analytics.sales_by_company || {}),
        backgroundColor: "rgba(75, 192, 192, 0.6)",
      },
    ],
  };

  const yearData = {
    labels: Object.keys(analytics.records_by_year || {}),
    datasets: [
      {
        label: "Records by Year",
        data: Object.values(analytics.records_by_year || {}),
        borderColor: "rgba(153, 102, 255, 1)",
        fill: false,
      },
    ],
  };

  return (
    <>
      <h2 style={{ color: "black", fontSize: "2rem", 
        fontWeight: "bold", 
        textAlign: "center",
        marginTop: "2rem",
        marginBottom: "2rem",
        marginRight:"70rem",

       }}>
  Sales by Company
</h2>

      <Bar data={salesData} />

      <h2 style={{ color: "black", fontSize: "2rem", 
        fontWeight: "bold", 
        textAlign: "center",
        marginTop: "2rem",
        marginBottom: "2rem",
        marginRight:"70rem",

       }}>
  Records by Year
</h2>
      <Line data={yearData} />
    </>
  );
}
