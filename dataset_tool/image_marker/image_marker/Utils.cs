using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;

namespace image_marker
{
    class Utils
    {
        public static List<String> Classes = null;

        /// <summary>
        /// initialize keys from image folder
        /// </summary>
        /// <param name="path"></param>
        /// <returns></returns>
        public static Dictionary<String, List<BoundingBox>> LoadFromDir(String path)
        {
            Dictionary<String, List<BoundingBox>> dict = new Dictionary<string, List<BoundingBox>>();

            String[] flist = Directory.GetFiles(path, "*.*", SearchOption.AllDirectories);

            foreach (String f in flist)
            {
                dict.Add(f, new List<BoundingBox>());
            }

            return dict;
        }

        /// <summary>
        /// load exsiting data from annotation file, can be edited after you save your marking work
        /// </summary>
        /// <param name="path"></param>
        /// <returns></returns>
        public static Dictionary<String, List<BoundingBox>> LoadFromAnnotationFile(String path)
        {
            /* [annotation file format]
             * row format   : image_path box1 box2 box3 ... boxN
             * box format   : left,top,right,bottom,class_id
             * 
             * example:
             * .\dataset\training_images\1.jpg 100,86,230,203,0 300,98,640,256,3 
             * .\dataset\training_images\2.jpg 200,186,435,505,2 120,28,243,116,8
             * .......
             */

            using (FileStream fs = new FileStream(path, FileMode.Open, FileAccess.Read))
            {
                StreamReader reader = new StreamReader(fs);
                Dictionary<String, List<BoundingBox>> dict = new Dictionary<string, List<BoundingBox>>();

                String line = null;
                String[] cols = null;
                String[] items = null;
                String key = null;

                while (!reader.EndOfStream)
                {
                    line = reader.ReadLine();

                    cols = line.Split(' ');

                    if (cols != null && cols.Length >= 2)
                    {
                        for (int i = 1; i < cols.Length; ++i)
                        {
                            items = cols[i].Split(',');

                            if (items.Length == 5)
                            {
                                key = cols[0];

                                if (!dict.ContainsKey(key))
                                {
                                    dict.Add(key, new List<BoundingBox>());
                                }

                                dict[key].Add(new BoundingBox() { IsSelected = false, Image_Path = key, Region = new System.Drawing.Rectangle(int.Parse(items[0]), int.Parse(items[1]), int.Parse(items[2]) - int.Parse(items[0]), int.Parse(items[3]) - int.Parse(items[1])), Class_ID = int.Parse(items[4]) });
                            }
                        }
                    }
                }

                return dict;
            }
            
        }

        /// <summary>
        /// load classes from default_classes.txt
        /// </summary>
        /// <param name="path"></param>
        /// <returns></returns>
        public static bool LoadClassesData(String path)
        {
            List<String> l = new List<string>();

            using (FileStream fs = new FileStream(path, FileMode.Open, FileAccess.Read))
            {
                StreamReader reader = new StreamReader(fs);
                String line = null;

                while (!reader.EndOfStream)
                {
                    line = reader.ReadLine();

                    l.Add(line);
                }
                Classes = l;
            }

            return l.Count != 0;
        }
    }
}
