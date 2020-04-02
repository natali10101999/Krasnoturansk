using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace WpfApp1
{
    /// <summary>
    /// Логика взаимодействия для MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
            quiz.Focus();

            var myModel = new WordCollection();
            myModel.Add(new Word() { En = "Run", Ru = "Бежать" });
            myModel.Add(new Word() { En = "Read", Ru = "Читать" });
            myModel.Add(new Word() { En = "Write", Ru = "Писать" });
            myModel.Add(new Word() { En = "Go", Ru = "Идти" });
            myModel.Add(new Word() { En = "Think", Ru = "Думать" });
            myModel.Add(new Word() { En = "Walk", Ru = "Гулять" });
            this.DataContext = myModel;
        }
    }
}
