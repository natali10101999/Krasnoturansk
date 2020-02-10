using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;
namespace ConvertDict
{
    class Dict
    {
        public Dictionary<string, DictEntry> Words;
        public static Dict Load(string path)
        {
            var res = new Dict();
            res.Words = new Dictionary<string, DictEntry>();
            var text = File.ReadAllText(path).Split(new string[] { "_____\n\n" }, StringSplitOptions.None);
            foreach (var entry in text)
            {
                if (entry.StartsWith("@")) continue;
                var dictEntry = DictEntry.Parse(entry);

                if (res.Words.ContainsKey(dictEntry.Word)) continue;

                res.Words.Add(dictEntry.Word, dictEntry);
                
            }

            return res;
        }
    }

    class DictEntry
    {
        public string Word;
        public string Description;
        public static DictEntry Parse(string entry) 
        {
            var i = entry.IndexOf("\n\n"); 
            var res = new DictEntry();
            res.Word = entry.Substring(0, i);
            res.Description = entry.Substring(i + 2);
            return res;
        }
    }
}
