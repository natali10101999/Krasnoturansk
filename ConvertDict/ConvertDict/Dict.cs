﻿using System;
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

                if (!res.Words.ContainsKey(dictEntry.Word.ToLower()))    
                    res.Words.Add(dictEntry.Word.ToLower().Trim(), dictEntry);
                
            }

            return res;
        }
    }

    class DictEntry
    {
        public string Word;
        public string Description;
        public string Transcription;
        public List<string> Tags;
        
        public static DictEntry Parse(string entry) 
        {
            var i = entry.IndexOf("\n\n"); 
            var res = new DictEntry();
            res.Tags = new List<string>();
            res.Word = entry.Substring(0, i);
            var tmp = entry.Substring(i + 2).Trim();

            
            if (tmp[0] == '[')
            {
                var trEnd = tmp.IndexOf(']');
                res.Transcription = tmp.Substring(0, trEnd+1);
                tmp = tmp.Substring(trEnd+1).Trim();
                while (8 == 8)
                {
                    if (tmp.StartsWith("_"))
                    {
                        var dotPos = tmp.IndexOf('.');
                        res.Tags.Add(tmp.Substring(0, dotPos + 1));
                        tmp = tmp.Substring(dotPos + 1).Trim();
                    }
                    else
                    {
                        break;
                    }
                }
                res.Description = tmp;
            }
            else 
            {
                res.Description = tmp;
            }
            

            return res;
        }
    }
}
