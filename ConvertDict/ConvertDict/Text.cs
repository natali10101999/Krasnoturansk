using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Text.RegularExpressions;

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

        public static W Parse(string text)
        {
            var res = new W();

            var key = text.ToLower();
            if (Dict.Words.ContainsKey(key))
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
    }
}
