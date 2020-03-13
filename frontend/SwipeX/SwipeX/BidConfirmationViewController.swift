//
//  BidConfirmationViewController.swift
//  SwipeX
//
//  Created by Ashwin Vivek on 3/11/20.
//  Copyright © 2020 CS 130. All rights reserved.
//

import UIKit
import Alamofire

class BidConfirmationViewController: UIViewController {

    var price:Int?
    var meetupTimeString:String?
    @IBOutlet weak var priceLabel: UILabel!
    @IBOutlet weak var meetupTimes: UILabel!
    var hallId:Int?
    var startTime:String?
    var endTime:String?
    
    @IBAction func confirmPressed(_ sender: Any) {
        let userId = UserDefaults.standard.integer(forKey: "userId")
        let parameters = [
            "user_id": userId,
            "hall_id": hallId,
            "desired_price": price,
            "time_intervals":[
                [
                    "start":startTime,
                    "end":endTime
                ]
            ]
        ] as [String : Any]
        
        // Stripe processing.
        
        AF.request("\(NGROK_URL)/api/buying/buy/", method:.post, parameters: parameters, encoding:JSONEncoding.default).responseJSON { response in
            switch response.result {
                case .success:
                    if let value = response.value as? NSDictionary {
                        print(value)
                        self.dismiss(animated: true, completion: nil)
                    }
                case let .failure(error):
                    print(error)
            }
        }
        
    }
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
        
        priceLabel.text = "$ \(price!)"
        meetupTimes.text = meetupTimeString
    }
    

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destination.
        // Pass the selected object to the new view controller.
    }
    */

}
