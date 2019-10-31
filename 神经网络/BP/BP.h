#include<iostream>
#include <vector>  
#include <assert.h>
using namespace std;

#define LAYER    3        //三层神经网络  
#define NUM      10       //每层的最多节点数  

#define A        40.0  
#define B        20.0     //A和B是S型函数的参数  
#define ITERS    1000      //最大训练次数  
#define ETA_W    0.0035   //权值调整率  
#define ETA_B    0.001    //阀值调整率  
#define mERROR    0.002    //单个样本允许的误差  
#define ACCU     0.005    //每次迭代允许的误差  

#define Type double  
#define Vector std::vector  

vector<pair<int,double>>coordinate;
vector<pair<int,double>>::iterator ptr;
struct Data  
{  
	Vector<Type> x;       //输入数据  
	Vector<Type> y;       //输出数据  
};  

class BP{  

public:  

	void GetData(const Vector<Data>);  
	void Train();  
	Vector<Type> ForeCast(const Vector<Data>);  

private:  

	void InitNetWork();         //初始化网络  
	void GetNums();             //获取输入、输出和隐含层节点数  
	void ForwardTransfer();     //正向传播子过程  
	void ReverseTransfer(int);  //逆向传播子过程  
	void CalcDelta(int);        //计算w和b的调整量  
	void UpdateNetWork();       //更新权值和阀值  
	Type GetError(int);         //计算单个样本的误差  
	Type GetAccu();             //计算所有样本的精度  
	Type Sigmoid(const Type);   //计算Sigmoid的值  

private:  
	int in_num;                 //输入层节点数  
	int ou_num;                 //输出层节点数  
	int hd_num;                 //隐含层节点数  

	Vector<Data> data;          //输入输出数据  

	Type w[LAYER][NUM][NUM];    //BP网络的权值  
	Type b[LAYER][NUM];         //BP网络节点的阀值  

	Type x[LAYER][NUM];         //每个神经元的值经S型函数转化后的输出值，输入层就为原值  
	Type d[LAYER][NUM];         //记录delta学习规则中delta的值  
};  

void BP::GetData(const Vector<Data> _data)  
{  
	data = _data;  
}  

//开始进行训练  

void BP::Train()  
{  
	//cout<<"Begin to train BP NetWork!\n";  
	GetNums();  
	InitNetWork();  
	int num = data.size();  
	for(int iter = 0; iter <= ITERS; iter++)  
	{  
		for(int cnt = 0; cnt < num; cnt++)  
		{  
			//第一层输入节点赋值  
			for(int i = 0; i < in_num; i++)  
				x[0][i] = data.at(cnt).x[i];  

			//while(1)  
			//{  
				ForwardTransfer();       
				//if(GetError(cnt) < ERROR)    //如果误差比较小，则针对单个样本跳出循环  
				//	break;  
				ReverseTransfer(cnt);    
			//}  
		}  
		//cout<<"This is the %d th trainning NetWork !\n"<<iter;  

		Type accu = GetAccu();
		coordinate.push_back(pair<int,double>(iter, accu));
		//cout<<"All Samples Accuracy is \n"<<accu; 

		if(accu < ACCU) break;  
	}  
	//for (ptr = coordinate.begin(); ptr != coordinate.end(); ptr++)
	//{
	//	cout<<ptr->first<<" "<<ptr->second<<endl;
	//}
	//cout<<"The BP NetWork train End!\n";  
}  

//根据训练好的网络来预测输出值  
Vector<Type> BP::ForeCast(const Vector<Data> data)  
{  
	Vector<Type> v; 
	int n = data.size();  
	//assert(n == in_num);  
	for(int i = 0; i < n; i++)
	{
		for(int j=0; j<3; j++)
		{
			x[0][j] = data.at(i).x[j];
		}
		ForwardTransfer();   
		for(int i = 0; i < ou_num; i++) 
			v.push_back(x[2][i]);  
	} 
	return v; 
}  

//获取网络节点数  
void BP::GetNums()  
{  
	in_num = data[0].x.size();                         //获取输入层节点数  
	ou_num = data[0].y.size();                         //获取输出层节点数  
	hd_num = (int)sqrt((in_num + ou_num) * 1.0) + 5;   //获取隐含层节点数  
	if(hd_num > NUM) hd_num = NUM;                     //隐含层数目不能超过最大设置  
}  

//初始化网络  
void BP::InitNetWork()  
{  
	memset(w, 0, sizeof(w));      //初始化权值和阀值为0，也可以初始化随机值  
	memset(b, 0, sizeof(b));  
}  

//工作信号正向传递子过程  
void BP::ForwardTransfer()  
{  
	//计算隐含层各个节点的输出值  
	for(int j = 0; j < hd_num; j++)  
	{  
		Type t = 0;  
		for(int i = 0; i < in_num; i++)  
			t += w[1][i][j] * x[0][i];  
		t += b[1][j];  
		x[1][j] = Sigmoid(t);  
	}  

	//计算输出层各节点的输出值  
	for(int j = 0; j < ou_num; j++)  
	{  
		Type t = 0;  
		for(int i = 0; i < hd_num; i++)  
			t += w[2][i][j] * x[1][i];  
		t += b[2][j];  
		x[2][j] = Sigmoid(t);  
	}  
}  

//计算单个样本的误差  
Type BP::GetError(int cnt)  
{  
	Type ans = 0;  
	for(int i = 0; i < ou_num; i++)  
		ans += 0.5 * (x[2][i] - data.at(cnt).y[i]) * (x[2][i] - data.at(cnt).y[i]);  
	return ans;  
}  

//误差信号反向传递子过程  
void BP::ReverseTransfer(int cnt)  
{  
	CalcDelta(cnt);     
	UpdateNetWork();  
}  

//计算所有样本的精度  
Type BP::GetAccu()  
{  
	Type ans = 0;  
	int num = data.size();  
	for(int i = 0; i < num; i++)  
	{  
		int m = data.at(i).x.size();  
		for(int j = 0; j < m; j++)  
			x[0][j] = data.at(i).x[j];  
		ForwardTransfer();  
		int n = data.at(i).y.size();  
		for(int j = 0; j < n; j++)  
			ans += 0.5 * (x[2][j] - data.at(i).y[j]) * (x[2][j] - data.at(i).y[j]);  
	}  
	return ans / num;  
}  

//计算调整量  
void BP::CalcDelta(int cnt)  
{  
	//计算输出层的delta值  
	for(int i = 0; i < ou_num; i++)  
		d[2][i] = (x[2][i] - data.at(cnt).y[i]) * x[2][i] * (A - x[2][i]) / (A * B);  
	//计算隐含层的delta值  
	for(int i = 0; i < hd_num; i++)  
	{  
		Type t = 0;  
		for(int j = 0; j < ou_num; j++)  
			t += w[2][i][j] * d[2][j];  
		d[1][i] = t * x[1][i] * (A - x[1][i]) / (A * B);  
	}  
}  

//根据计算出的调整量对BP网络进行调整  
void BP::UpdateNetWork()  
{  
	//隐含层和输出层之间权值和阀值调整  
	for(int i = 0; i < hd_num; i++)  
	{  
		for(int j = 0; j < ou_num; j++)  
			w[2][i][j] -= ETA_W * d[2][j] * x[1][i];   
	}  
	for(int i = 0; i < ou_num; i++)  
		b[2][i] -= ETA_B * d[2][i];  

	//输入层和隐含层之间权值和阀值调整  
	for(int i = 0; i < in_num; i++)  
	{  
		for(int j = 0; j < hd_num; j++)  
			w[1][i][j] -= ETA_W * d[1][j] * x[0][i];  
	}  
	for(int i = 0; i < hd_num; i++)  
		b[1][i] -= ETA_B * d[1][i];  
}  

//计算Sigmoid函数的值  
Type BP::Sigmoid(const Type x)  
{  
	return A / (1 + exp(-x / B));  
}