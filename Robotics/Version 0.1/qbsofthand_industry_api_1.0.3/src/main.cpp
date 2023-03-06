/***
 *  Software License Agreement: BSD 3-Clause License
 *
 *  Copyright (c) 2019, qbrobotics®
 *  All rights reserved.
 *
 *  Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
 *  following conditions are met:
 *
 *  * Redistributions of source code must retain the above copyright notice, this list of conditions and the
 *    following disclaimer.
 *
 *  * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
 *    following disclaimer in the documentation and/or other materials provided with the distribution.
 *
 *  * Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote
 *    products derived from this software without specific prior written permission.
 *
 *  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
 *  INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 *  DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 *  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
 *  SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
 *  WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
 *  USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

#include <qbsofthand_industry_api/qbsofthand_industry_api.h>
#include <iomanip>
#include <iostream>
#include <thread>
#include <fstream>
#include <string>
using namespace std;

int main(int argc, char** argv) {
	cout << "I am here" << endl;  
	string position;	
	//string curPosition;
  	qbsofthand_industry_api::qbSoftHandIndustryAPI api_test;
 	int last_pos; 
	last_pos = -1;
  
  	if(!api_test.isInitialized()) {
		return -1;
  	}
	while (api_test.isInitialized()){

		//cout << api_test.getStatistics() << endl;
	
	  	//cout << setprecision(3) << "Start position: " << api_test.getPosition() << "%" << endl;
		ifstream Myfile("hand.txt");
		getline(Myfile, position);
		Myfile.close();
		int pos = stoi(position);
		cout << pos << " : " << last_pos << endl;
		//float curpos = api_test.getPosition();
		if (pos != last_pos) {
			cout << api_test.getStatistics() << endl;
	  		cout << setprecision(3) << "Start position: " << api_test.getPosition() << "%" << endl;
	  		//cout << setprecision(3) << "Start position: " << curpos << "%" << endl;
			cout << "position is: " << position << endl;
			cout << pos << endl;
		
			api_test.setClosure(pos, 50, 62.5);  // fully close the hand at half speed and minimum applied force (62.5% of max force is the minimum value that can be set)
			api_test.waitForTargetReached();
			last_pos = pos;
		}
		//Get current hand position and write to text file
		//curPosition = to_string(curpos);
		ofstream outfile;
		outfile.open("curhand.txt");
		//Myfile << curPosition;
		outfile << api_test.getPosition();
		outfile.close();

  		this_thread::sleep_for(std::chrono::seconds(1));
	}
  //this_thread::sleep_for(std::chrono::seconds(3));
  //cout << setprecision(3) << "Closed position: " << api_test.getPosition() << "%" << endl;

  //api_test.setClosure(0, 100, 100);  // reopen at full speed and full force
  //cout << "opening to 100%" << endl;
  //api_test.waitForTargetReached();
  //this_thread::sleep_for(chrono::seconds(3));
  //cout << setprecision(3) << "End position: " << api_test.getPosition() << "%" << endl;

  return 0;
}
