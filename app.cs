using System;
using System.Windows.Forms;
using System.Collections.Generic;

namespace MathApp
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void buttonCalculate_Click(object sender, EventArgs e)
        {
            try
            {
                int a = int.Parse(textBoxA.Text);
                int b = int.Parse(textBoxB.Text);
                int N = int.Parse(textBoxN.Text);
                int d = int.Parse(comboBoxD.SelectedItem.ToString());

                if (a > b)
                {
                    MessageBox.Show("Liczba a musi być mniejsza lub równa liczbie b");
                    return;
                }

                var results = GenerateTable(a, b, N, d);
                DisplayTable(results);
            }
            catch (Exception ex)
            {
                MessageBox.Show("Proszę podać prawidłowe wartości: " + ex.Message);
            }
        }

        // Funkcje matematyczne
        private Dictionary<string, double> MathFunctions(int x, int d)
        {
            return new Dictionary<string, double>
            {
                { "sin(x)", Math.Sin(x) },
                { "cos(x)", Math.Cos(x) },
                { "tan(x)", Math.Tan(x) },
                { "sqrt(|x|)", Math.Sqrt(Math.Abs(x)) },
                { "x^d", Math.Pow(x, d) },
                { "ln(|x|)", x != 0 ? Math.Log(Math.Abs(x)) : double.NaN }
            };
        }

        // Generowanie wyników
        private List<string[]> GenerateTable(int a, int b, int N, int d)
        {
            Random random = new Random();
            var results = new List<string[]>();

            for (int i = 0; i < N; i++)
            {
                int x = random.Next(a, b + 1);
                var functions = MathFunctions(x, d);
                results.Add(new string[]
                {
                    x.ToString(),
                    functions["sin(x)"].ToString("F2"),
                    functions["cos(x)"].ToString("F2"),
                    functions["tan(x)"].ToString("F2"),
                    functions["sqrt(|x|)"].ToString("F2"),
                    functions["x^d"].ToString("F2"),
                    functions["ln(|x|)"].ToString("F2")
                });
            }

            return results;
        }

        // Wyświetlanie wyników w tabeli
        private void DisplayTable(List<string[]> results)
        {
            dataGridViewResults.Rows.Clear();

            foreach (var result in results)
            {
                dataGridViewResults.Rows.Add(result);
            }
        }
    }
}
