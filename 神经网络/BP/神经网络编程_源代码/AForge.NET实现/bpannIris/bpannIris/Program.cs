using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;

using AForge;
using AForge.Neuro;
using AForge.Neuro.Learning;
using AForge.Controls;

namespace bpannIris
{
    class Program
    {
        private static double premnmx( double num , double min , double max  )
        {
            if (num > max)
                num = max;
            if (num < min)
                num = min; 

            return 2*(num - min) / (max - min) - 1;
        }

        private static double premnmx1(double num, double min, double max)
        {
            if (num > max)
                num = max;
            if (num < min)
                num = min;

            return (num - min) / (max - min);
        }
        
        static void Main(string[] args)
        {
            int trainNum = 75 ; 
            int testNum = 75 ; 
            double [][] trainInput = new double[trainNum][] ;
            double[][] trainOutput = new double[trainNum][];

            double [] max = new double [4] ; 
            double [] min = new double [4] ;
            for (int i = 0; i < 4; ++i)
            {
                max[i] = double.MinValue;
                min[i] = double.MaxValue; 
            }

            // 读取训练数据
            StreamReader reader = new StreamReader("trainData.txt");

            for (int i = 0; i < trainNum; ++i)
            {
                string value = reader.ReadLine();

                string[] temp = value.Split('\t');

                trainInput[i] = new double[4] ;
                trainOutput[i] = new double[3] ;

                for (int j = 0; j < 4; ++j)
                {
                    trainInput[i][j] = double.Parse(temp[j]);
                    if (trainInput[i][j] > max[j])
                        max[j] = trainInput[i][j];

                    if (trainInput[i][j] < min[j])
                        min[j] = trainInput[i][j];
                }
                for (int j = 0; j < 3; ++j)
                    trainOutput[i][j] = 0;
                trainOutput[i][ int.Parse( temp[4]  ) -1 ] = 1; 
            }

            // 归一化
            for (int i = 0; i < trainNum; ++i)
            {
                for (int j = 0; j < 4; ++j)
                {
                    trainInput[i][j] = premnmx(trainInput[i][j], min[j], max[j]);
                }
            }
            
            //训练网络

            // create multi-layer neural network
            ActivationNetwork network = new ActivationNetwork( new SigmoidFunction(3), 4, 5, 3 );
            // create teacher
            BackPropagationLearning teacher = new BackPropagationLearning(network);
            // set learning rate and momentum
            teacher.LearningRate = 0.1;
            teacher.Momentum = 0;

            int iteration = 1 ; 

            while( iteration < 500 ) 
            {
                teacher.RunEpoch( trainInput , trainOutput ) ; 
                ++iteration ;
            }


            // 读取测试数据

            double [][] testInput = new double [testNum][] ;
            double [] testOutput = new double [testNum] ;
            StreamReader reader1 = new StreamReader("testData.txt");
            for (int i = 0; i < testNum; ++i)
            {
                string value = reader1.ReadLine();

                string[] temp = value.Split('\t');

                testInput[i] = new double[4] ;

                for (int j = 0; j < 4; ++j)
                {
                    testInput[i][j] = double.Parse(temp[j]);
                }
                testOutput[i] = int.Parse(temp[4]);
            }

            // 对测试数据进行分类， 并统计正确率
            int hitNum = 0 ;
            for( int i = 0 ;  i < testNum ; ++i ) 
            {

                double[] inp = new double[4]{ testInput[i][0] , testInput[i][1] , testInput[i][2] ,testInput[i][3] } ;
                for (int j = 0; j < 4; ++j)
                    inp[j] = premnmx(inp[j], min[j], max[j]);

                double[] t = { inp[0], inp[1], inp[2], inp[3] };

                // 使用网络对训练样本计算输出
                double[] result =  network.Compute(t) ;

                int m = 0; 
                for( int j = 0 ; j < 3 ; ++j ) 
                    if( result[j] > result[m] ) 
                        m = j ; 
                
                if ( m  + 1 == testOutput[i])
                    ++hitNum;
            }

            System.Console.WriteLine("分类正确率为 {0}% ", 100.0 * hitNum /  testNum );
            System.Console.Read();
        }
    }
}
