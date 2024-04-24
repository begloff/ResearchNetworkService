using System;
using System.Diagnostics;
using System.IO;
using System.ServiceProcess;
using System.Timers;

namespace NetworkService
{
    public partial class Service1 : ServiceBase
    {
        private Timer timer = new Timer(); // Define timer at the class level

        public Service1()
        {
            InitializeComponent();
        }

        protected override void OnStart(string[] args)
        {
            WriteToFile("Service is started at " + DateTime.Now);
            timer.Elapsed += new ElapsedEventHandler(OnElapsedTime);
            timer.Interval = 600000; // Set the interval to every 10 min
            timer.Enabled = true;

            OnElapsedTime(null, null); //Run Event immediately after starting script
        }

        protected override void OnStop()
        {
            WriteToFile("Service is stopped at " + DateTime.Now);
        }

        private void OnElapsedTime(object source, ElapsedEventArgs e)
        {
            string message = $"{DateTime.Now} - ";

            try
            {
                WriteToFile($"{DateTime.Now} - STARTING SCRIPT EXECUTION UPDATED");
                string executablePath = "PythonScripts/testScript.exe";
                string logFilePath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "Logs", $"Output_{DateTime.Now.Ticks}.txt");
                string output = RunExecutable(executablePath, "", logFilePath);
                WriteToFile(output); // Write only the output to the file
            }
            catch (Exception ex)
            {
                WriteToFile($"Error executing testScript.exe: {ex.Message}");
            }
        }

        public void WriteToFile(string message)
        {
            string path = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "Logs");
            string filename = $"ServiceLog_{DateTime.Now:yyyy-MM-dd}.txt";
            string filepath = Path.Combine(path, filename);

            if (!Directory.Exists(path))
            {
                Directory.CreateDirectory(path);
            }

            // Create the log message with date and time
            string logMessage = $"{DateTime.Now} - {message}";


            // Append the log message to the file
            using (StreamWriter sw = File.AppendText(filepath))
            {
                sw.WriteLine(logMessage);
            }
        }

        public string RunExecutable(string executablePath, string arguments, string logFilePath)
        {
            ProcessStartInfo startInfo = new ProcessStartInfo();
            startInfo.FileName = executablePath;
            startInfo.Arguments = arguments;
            startInfo.UseShellExecute = false;
            startInfo.RedirectStandardOutput = true;
            startInfo.CreateNoWindow = true;

            using (Process process = new Process())
            {
                process.StartInfo = startInfo;
                process.Start();
                string output = process.StandardOutput.ReadToEnd(); // Read the entire output
                process.WaitForExit();
                return output; // Return the output
            }
        }
    }
}
