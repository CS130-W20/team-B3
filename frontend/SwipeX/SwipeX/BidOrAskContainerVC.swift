//
//  BidOrAskContainerVC.swift
//  SwipeX_2
//
//  Created by Ashwin Vivek on 2/20/20.
//  Copyright © 2020 CS 130. All rights reserved.
//

import UIKit
import Alamofire

class BidOrAskContainerVC: UIViewController, SwipeInfoDelegate {
    func gotSwipeInfo(info: NSDictionary) {
        return
    }
    
    func gotPrice(price: Int) {
        self.price = price
    }
    
    
    weak var parentVC: BuyOrSellViewController?
    
    let timePickerFrom = ToolbarDatePicker()
    let timePickerTo = ToolbarDatePicker()
    
    @IBOutlet weak var fromTimeField: UITextField!
    @IBOutlet weak var toTimeField: UITextField!
    
    var isBidding:Bool?
    var didTapFrom: Bool?
    var hallId:Int!
    var price:Int!
    
    @IBOutlet weak var titleLabel: UILabel!
    @IBAction func didTapFrom(_ sender: Any) {
        didTapFrom = true
    }
    @IBAction func didTapTo(_ sender: Any) {
        didTapFrom = false
    }
    
    @IBOutlet weak var actionButton: UIButton!
    
    @objc func keyboardWillShow(notification: NSNotification) {
        if view.frame.origin.y == 0 {
            view.frame.origin.y -= timePickerTo.frame.height
            print(timePickerTo.frame.height)
        }
    }

    @objc func keyboardWillHide(notification: NSNotification) {
        if view.frame.origin.y != 0 {
            view.frame.origin.y = 0
        }
    }
    
    @IBAction func buttonPressed(_ sender: Any) {
        let userId = UserDefaults.standard.integer(forKey: "userId")
        let parameters = [
            "user_id": userId,
            "hall_id": hallId,
            "desired_price": parentVC!.priceField.text,
            "time_intervals":[
                [
                    "start":convertPickerTimeToJSONString(time: timePickerFrom.date),
                    "end":convertPickerTimeToJSONString(time: timePickerTo.date)
                ]
            ]
        ]
            as [String : Any]
        if (isBidding!) {
            AF.request("\(NGROK_URL)/api/buying/buy/", method:.post, parameters: parameters, encoding:JSONEncoding.default).responseJSON { response in
                    switch response.result {
                        case .success:
                            if let value = response.value as? NSDictionary {
        //                        if let data = value.data(using: String.Encoding.utf8) {
        //                            let json = JSON(data)
                                print(value)
                                self.performSegue(withIdentifier: "bidToPaymentSegue", sender: self)
                            }
                        case let .failure(error):
                            print(error)
                    }
                }
        } else {
            
            AF.request("\(NGROK_URL)/api/selling/sell/", method:.post, parameters: parameters, encoding:JSONEncoding.default).responseJSON { response in
                        switch response.result {
                            case .success:
                                if let value = response.value as? NSDictionary {
            //                        if let data = value.data(using: String.Encoding.utf8) {
            //                            let json = JSON(data)
                                    print(value)
                                    self.navigationController?.popToRootViewController(animated: true)
                                }
                            case let .failure(error):
                                print(error)
                        }
                    }
            }
    }
    
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        if (segue.identifier == "bidToPaymentSegue") {
            let vc: BidConfirmationViewController = segue.destination as! BidConfirmationViewController
            
            var timeFormatter = DateFormatter()

            timeFormatter.dateStyle = DateFormatter.Style.none
            timeFormatter.timeStyle = DateFormatter.Style.short
            timeFormatter.dateFormat = "HH:mm"
            
            vc.meetupTimeString = "\(timeFormatter.string(from: timePickerFrom.date)) - \(timeFormatter.string(from: timePickerTo.date))"
            vc.price = price
        }
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        if (isBidding!) {
            titleLabel.text = "Bid for one swipe for..."
            actionButton.backgroundColor = #colorLiteral(red: 0.3411764801, green: 0.6235294342, blue: 0.1686274558, alpha: 1)
            actionButton.setTitle("Bid now", for: .normal)
        } else {
            titleLabel.text = "Offer one swipe for..."
            actionButton.backgroundColor = #colorLiteral(red: 0.9379594326, green: 0.2973573804, blue: 0.3231473565, alpha: 1)
           actionButton.setTitle("Offer now", for: .normal)
        }
        
        NotificationCenter.default.addObserver(self, selector: #selector(self.keyboardWillShow), name: UIResponder.keyboardWillShowNotification, object: nil)
        NotificationCenter.default.addObserver(self, selector: #selector(self.keyboardWillHide), name: UIResponder.keyboardWillHideNotification, object: nil)
        
        self.fromTimeField.inputView = self.timePickerFrom
        self.toTimeField.inputView = self.timePickerTo
        
        self.fromTimeField.inputAccessoryView = self.timePickerFrom.toolbar
        self.toTimeField.inputAccessoryView = self.timePickerTo.toolbar
        
        self.timePickerFrom.datePickerMode = UIDatePicker.Mode.time
        self.timePickerTo.datePickerMode = UIDatePicker.Mode.time
        
        self.timePickerFrom.minuteInterval = 15
        self.timePickerTo.minuteInterval = 15

        self.timePickerFrom.toolbarDelegate = self
        self.timePickerTo.toolbarDelegate = self
        
        let timeFormatter = DateFormatter()
        timeFormatter.dateStyle = DateFormatter.Style.none
        timeFormatter.timeStyle = DateFormatter.Style.short
        
        fromTimeField.text = timeFormatter.string(from:timePickerFrom.date)
        toTimeField.text = timeFormatter.string(from:timePickerTo.date)
        // Do any additional setup after loading the view.
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

extension BidOrAskContainerVC: ToolbarDatePickerDelegate {

    func didTapDone() {
        var timeFormatter = DateFormatter()
        timeFormatter.dateStyle = DateFormatter.Style.none
        timeFormatter.timeStyle = DateFormatter.Style.short

        if (self.didTapFrom!) {
            fromTimeField.text = timeFormatter.string(from: self.timePickerFrom.date)
            self.timePickerTo.minimumDate = self.timePickerFrom.date.addingTimeInterval(15.0)
            self.fromTimeField.resignFirstResponder()

        } else {
            toTimeField.text = timeFormatter.string(from: self.timePickerTo.date)
            self.timePickerFrom.maximumDate = self.timePickerTo.date.addingTimeInterval(-15.0)
            self.toTimeField.resignFirstResponder()
        }
        // TODO: Filter the best ask and bid
    }
    
    func didTapCancel() {
        if(self.didTapFrom!) {
            self.fromTimeField.resignFirstResponder()
        } else {
            self.toTimeField.resignFirstResponder()
        }
    }
}
