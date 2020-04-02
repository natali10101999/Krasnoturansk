using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Globalization;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Data;
using System.Windows.Input;

namespace WpfApp1
{
    class Word : INotifyPropertyChanged
    {
        public string En { get; set; }
        public string Ru { get; set; }    
        public string UserAnswer { get; set; } 
        public IndicationMode Mode { get; set; }

        public event PropertyChangedEventHandler PropertyChanged;

        public void Check()
        {
            if (string.IsNullOrEmpty(UserAnswer))
            {
                Mode = IndicationMode.Normal;
            }
            else if (UserAnswer.ToLower() == Ru.ToLower())
            {
                Mode = IndicationMode.Correct;
            }
            else
            {
                Mode = IndicationMode.Error;
            }
            var a = PropertyChanged;
            if (a != null)
            {
                a(this, new PropertyChangedEventArgs("Mode"));
            }
            
        }

    }

    class WordCollection : List<Word>, INotifyPropertyChanged
    {
        MyCommand prev;
        MyCommand next;
        MyCommand first;
        MyCommand last;
        MyCommand enter;

        public event PropertyChangedEventHandler PropertyChanged;

        public WordCollection()
        {
            prev = new MyCommand(MovePrev);
            next = new MyCommand(MoveNext);
            first = new MyCommand(MoveFirst);
            last = new MyCommand(MoveLast);
            enter = new MyCommand(TextEntered);
        }

        public int CurrentWordIndex { get; set; }

        public Word Current
        {
            get { return this[CurrentWordIndex]; }
        }

        public MyCommand Prev 
        {
            get { return prev; }
        }

        public MyCommand Next
        {
            get { return next; }
        }

        public MyCommand First
        {
            get { return first; }
        }

        public MyCommand Last
        { 
            get { return last; }
        }

        public MyCommand Enter
        {
            get { return enter; }
        }

        private void OnPropertyChanged(string propName)
        {
            var a = PropertyChanged;
            if (a != null)
            {
                a(this, new PropertyChangedEventArgs(propName));
            }
        }

        public void MovePrev()
        {
            if (CurrentWordIndex>0)
            {
                CurrentWordIndex--;
                OnPropertyChanged("Current");
                OnPropertyChanged("CurrentWordIndex");
            }
        }

        public void MoveNext()
        {
            if (CurrentWordIndex < this.Count - 1)
            {
                CurrentWordIndex++;
                OnPropertyChanged("Current");
                OnPropertyChanged("CurrentWordIndex");
            }
            
        }
        public void MoveFirst()
        {
            CurrentWordIndex = 0;
            OnPropertyChanged("Current");
            OnPropertyChanged("CurrentWordIndex");
        }
        public void MoveLast()
        {
            CurrentWordIndex = this.Count-1;
            OnPropertyChanged("Current");
            OnPropertyChanged("CurrentWordIndex");
        }
        public void TextEntered()
        {
            Current.Check();
        }
    }

    class MyCommand : ICommand
    {
        Action action;
        public MyCommand(Action action)
        {
            this.action = action;
        }
        public event EventHandler CanExecuteChanged;

        public bool CanExecute(object parameter)
        {
            return true;
        }

        public void Execute(object parameter)
        {
            action();
        }
    }

    class PlusOneConverter : IValueConverter
    {
        public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
        {
            return (int)value+1;
        }

        public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
        {
            throw new NotImplementedException();
        }
    }
    

}
