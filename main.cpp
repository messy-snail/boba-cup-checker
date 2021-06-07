#include <iostream>

#include "ColorFinder.h"
#include "CamManager.h"

using namespace std;
using namespace cv;

rainbow::vision::CamManager cm;

int main(){
    cout<<"Version: "<< CV_VERSION<<endl;
    if(cm.Open()){
        while(1){
            cm.Run();
        }
    }
    return 0;
}
