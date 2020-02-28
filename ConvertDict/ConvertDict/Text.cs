using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Text.RegularExpressions;
using System.Xml.Linq;
using ENRUSDict;

namespace ConvertDict
{
    /// <summary>
    /// абазц
    /// </summary>
    class P 
    {
        public List<S> Senteces;
        public static P Parse (string text)
        {
            var pp = text.Split(new string[] { "\r\n" }, StringSplitOptions.None);
            var res = new P();
            res.Senteces = new List<S>();
            foreach (var i in pp)
            {
                res.Senteces.Add(S.Parse(i));
            }

            return res;
        }
        public XElement Save()
        {
            var xRes = new XElement("p");
            foreach (var i in Senteces)
            {
                var xS = i.Save();
                xRes.Add(xS);
            }

            return xRes;
        }
    }
    /// <summary>
    /// Предложение
    /// </summary>
    class S
    {
        static Regex rx = new Regex("[A-Za-z]+(-[A-Za-z]+)*");
        public string Text;
        public List<W> Words;
        
        public static S Parse (string text)
        {
            var words = rx.Matches(text);
            var res = new S();
            res.Text = text;
            res.Words = new List<W>();
          
            foreach (var word in words)
            {
                var word2 = (word as Match).Value;
                res.Words.Add(W.Parse(word2));
            }
            return res;
        }

        public XElement Save()
        {
            var xRes = new XElement("s");
            xRes.Add(new XElement("t", Text));
            var xWords = new XElement("words");
            foreach (var i in Words)
            {
                var xW = i.Save();
                xWords.Add(xW);
            }

            xRes.Add(xWords);

            return xRes;
        }

        public override string ToString()
        {
            return Text;
        }
    }
    /// <summary>
    /// Слово
    /// </summary>
    class W
    {
        public string Key;
        public string Transcription;
        public string Article;

        public static Dict Dict;
        public static HashSet<string> StopWords;

        public static W Parse(string text)
        {
            var res = new W();
            var key = text.ToLower();

            if (Dict.Words.ContainsKey(key) /*&& !StopWords.Contains(key)*/)
            {
                var article = Dict.Words[text.ToLower()];
                res.Key = article.Word;
                res.Transcription = article.Transcription;
                res.Article = article.Description;
            }
            else
            {
                res.Key = key;
            }
            return res;
        }

        public XElement Save()
        {
            var xRes = new XElement("w");
            xRes.Value = Article ?? "";
            xRes.Add(new XAttribute("key", Key));
            xRes.Add(new XAttribute("t", Transcription ?? ""));
            return xRes;
        }

        public override string ToString()
        {
            return Key + " " + Article;
        }

    }
    class Text
    {
        public List<P> Paragraphs;
        public static Text Parse(string text)
        {
            var pp = text.Split(new string[] { "\r\n\r\n" }, StringSplitOptions.None);
            var res = new Text();
            res.Paragraphs = new List<P>();
            foreach (var i in pp)
            {
                res.Paragraphs.Add(P.Parse(i));
            }

            return res;
        }
        public XElement Save()
        {
            var xRes = new XElement("text");
            foreach (var i in Paragraphs)
            {
                var xP = i.Save();
                xRes.Add(xP);
            }

            return xRes;
        }
    }
}
