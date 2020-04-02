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
    public class QuizControl : Control
    {
        Dictionary<Key, string> rusKeyMap;
        public QuizControl()
        {
            this.Focusable = true;
            rusKeyMap = new Dictionary<Key, string>()
            {
                {Key.F,"А"},
                {Key.OemComma,"Б"},
                {Key.D,"В"},
                {Key.U,"Г"},
                {Key.L,"Д"},
                {Key.T,"Е"},
                {Key.Oem3,"Ё"},
                {Key.Oem1,"Ж"},
                {Key.P,"З"},
                {Key.B,"И"},
                {Key.Q,"Й"},
                {Key.R,"К"},
                {Key.K,"Л"},
                {Key.V,"М"},
                {Key.Y,"Н"},
                {Key.J,"О"},
                {Key.G,"П"},
                {Key.H,"Р"},
                {Key.C,"С"},
                {Key.N,"Т"},
                {Key.E,"У"},
                {Key.A,"Ф"},
                {Key.OemOpenBrackets,"Х"},
                {Key.W,"Ц"},
                {Key.X,"Ч"},
                {Key.I,"Ш"},
                {Key.O,"Щ"},
                {Key.Oem6,"Ъ"},
                {Key.S,"Ы"},
                {Key.M,"Ь"},
                {Key.OemQuotes,"Э"},
                {Key.OemPeriod,"Ю"},
                {Key.Z,"Я"},
            };
        }
        static QuizControl()
        {
            DefaultStyleKeyProperty.OverrideMetadata(typeof(QuizControl), new FrameworkPropertyMetadata(typeof(QuizControl)));
        }

        FormattedText FormatText(string text, Brush brush)
        {
            var t = text ?? "";
            return new FormattedText(t.Length == 0 ? " " : t, System.Globalization.CultureInfo.InvariantCulture, FlowDirection.LeftToRight,
                new Typeface("Arial"), 30, brush, VisualTreeHelper.GetDpi(this).PixelsPerDip);
        }

        protected override void OnRender(DrawingContext dc)
        {
            Brush background;
            Brush foreground;
            switch (Mode)
            {
                case IndicationMode.Normal: background = Brushes.White; foreground = Brushes.Black; break;
                case IndicationMode.Error: background = Brushes.Red; foreground = Brushes.White; break;
                case IndicationMode.Correct: background = Brushes.Green; foreground = Brushes.White; break;
                default: throw new NotImplementedException();

            }
            dc.DrawRectangle(background, null, new Rect(0, 0, this.ActualWidth, this.ActualHeight));
            var tx = FormatText(Text, foreground);
            var x = this.RenderSize.Width / 2 - tx.Width / 2;
            var y = this.RenderSize.Height / 2 - tx.Height / 2;

            dc.DrawText(tx, new Point(x, y));
            var sp = tx.Text.EndsWith(" ") ? 5 : 0;
            dc.DrawRectangle(foreground, null, new Rect(x + tx.Width + sp, y, 5, tx.Height));

        }

        protected override void OnKeyDown(KeyEventArgs e)
        {
            var t = (Text ?? "");

            if (rusKeyMap.ContainsKey(e.Key))
            {
                t += rusKeyMap[e.Key];
            }
            //if (e.Key >= Key.A && e.Key <= Key.Z)
            //{
            //    t += e.Key;
            //}
            else if (e.Key == Key.Back)
            {
                if (!string.IsNullOrEmpty(t))
                    t = t.Substring(0, t.Length - 1);
            }
            else if (e.Key == Key.Space)
            {
                if (!string.IsNullOrEmpty(t) && !t.EndsWith(" ")) t += " ";
            }
            else if (e.Key == Key.Enter)
            {
                TextEntered.Execute(null);
            }

            this.Text = t.Trim();

            InvalidateVisual();
        }
        protected override void OnMouseDown(MouseButtonEventArgs e)
        {
            this.Focus();
        }

        public string Text
        {
            get { return (string)GetValue(TextProperty); }
            set { SetValue(TextProperty, value); }
        }

        public static readonly DependencyProperty TextProperty =
            DependencyProperty.Register("Text", typeof(string), typeof(QuizControl), new PropertyMetadata("", OnTextChanged));

        static void OnTextChanged(DependencyObject d, DependencyPropertyChangedEventArgs e)
        {
            var _this = ((QuizControl)d);
            _this.InvalidateVisual();
        }

        public ICommand TextEntered
        {
            get { return (ICommand)GetValue(TextEnteredProperty); }
            set { SetValue(TextEnteredProperty, value); }
        }

        public static readonly DependencyProperty TextEnteredProperty =
            DependencyProperty.Register("TextEntered", typeof(ICommand), typeof(QuizControl), new PropertyMetadata(null));

        public IndicationMode Mode
        {
            get { return (IndicationMode)GetValue(ModeProperty); }
            set { SetValue(ModeProperty, value); }
        }

        public static readonly DependencyProperty ModeProperty =
            DependencyProperty.Register("Mode", typeof(IndicationMode), typeof(QuizControl), new PropertyMetadata(IndicationMode.Normal, OnModeChanged));
        
        static void OnModeChanged (DependencyObject d, DependencyPropertyChangedEventArgs e) 
        {
            ((QuizControl)d).InvalidateVisual();
        }
    }

    public enum IndicationMode { Normal, Error, Correct}
}
