using System;
using Windows.Globalization;
using Windows.Graphics.Imaging;
using Windows.Media.Ocr;
using System.IO;

//https://medium.com/rkttu/using-windows-10-built-in-ocr-with-c-b5ca8665a14e
//%windir%\Microsoft.NET\Framework64\v4.0.30319\System.Runtime.WindowsRuntime.dll
//%programfiles(x86)%\Windows Kits\10\UnionMetadata\10.0.19041.0
namespace winocr
{
    class Program
    {
        static async System.Threading.Tasks.Task Main(string[] args)
        {
            var loadResult = @".\lib_\loadResult.txt";
            var language = new Language("ja");
            if (!OcrEngine.IsLanguageSupported(language))
            {
                File.WriteAllText(loadResult, "False");
                throw new Exception($"{ language.LanguageTag } is not supported in this system.");
            }
            else
            {
                File.WriteAllText(loadResult, "True");
            }

            var inputPath = @".\lib_\input.jpg";
            var outputPath = @".\lib_\output.txt";
            if (File.Exists(inputPath))
            {
                var stream = File.OpenRead(inputPath);
                var decoder = await BitmapDecoder.CreateAsync(stream.AsRandomAccessStream());
                var bitmap = await decoder.GetSoftwareBitmapAsync();
                var engine = OcrEngine.TryCreateFromLanguage(language);
                var ocrResult = await engine.RecognizeAsync(bitmap).AsTask();
                Console.WriteLine(ocrResult.Text);
                File.WriteAllText(outputPath, ocrResult.Text);
            }
        }
    }
}
