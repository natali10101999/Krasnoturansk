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
            var text = File.ReadAllText(path);
            return res;
        }
    }

    class DictEntry
    {
        public string Word;
        public string Description;

    }
}
