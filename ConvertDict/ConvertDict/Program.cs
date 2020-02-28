using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using ENRUSDict;

namespace ConvertDict
{
    class Program
    {
        static void Main(string[] args)
        {
            var d = Dict.Load(@"..\..\..\..\Data\ENRUS.TXT");
            W.Dict = d;
            W.StopWords = new HashSet<string>(File.ReadAllLines(@"..\..\..\..\Data\StopWords.txt"));
            var txt = File.ReadAllText(@"..\..\..\..\Data\O'Henry.txt");
            var t = Text.Parse(txt);
            
            t.Save().Save(@"..\..\..\..\Data\O'Henry.xml");
        }

        private static void Abc()
        {
            //D:\Work\Krasnoturansk\ConvertDict\ConvertDict\bin\Debug\ConvertDict.exe
            //D:\Work\Krasnoturansk\mueller-dict-3.1.1\src\mueller-base 
            var d = Dict.Load(@"..\..\..\..\mueller-dict-3.1.1\src\mueller-base");
            //var sokr = Dict.Load(@"..\..\..\..\mueller-dict-3.1.1\src\mueller-dict");
            var txt = File.ReadAllText(@"..\..\..\..\Data\txt.txt");

            var rx = new Regex("[A-Za-z]+(-[A-Za-z]+)*");

            var words = rx.Matches(txt);
            var found = new List<string>();
            var notFound = new List<string>();

            foreach (var word in words)
            {
                var word2 = (word as Match).Value;
                if (d.Words.ContainsKey(word2.ToLower()))
                {
                    found.Add(word2);
                }
                else
                {
                    notFound.Add(word2);
                }
            }
        }
    }
}
