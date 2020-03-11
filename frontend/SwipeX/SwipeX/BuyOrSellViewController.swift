//
//  BuyOrSellViewController.swift
//  SwipeX_2
//
//  Created by Ashwin Vivek on 2/20/20.
//  Copyright © 2020 CS 130. All rights reserved.
//

import UIKit
import Alamofire

protocol SwipeInfoDelegate {
    func gotSwipeInfo(info: NSDictionary)
}

class BuyOrSellViewController: UIViewController, UITextFieldDelegate {

    @IBOutlet weak var containerViewBuyOrSell: UIView!
    @IBOutlet weak var containerViewBidOrAsk: UIView!
    
    @IBOutlet weak var priceField: UITextField!
    
    var isBuying:Bool?
    var priceValue:Int?
    let timePicker = ToolbarDatePicker()
    var minimumTime:Date?
    var maximumTime:Date?
    var matchAvailable:Bool?
    var diningHallName:String?
    var hallId:Int?
    var originPriceField:CGFloat?
    var dollarOrigin:CGFloat?
    
    var highestBid:Int?
    var lowestAsk:Int?
    
    var delegate:SwipeInfoDelegate?
    
    @IBOutlet weak var diningHallLabel: UILabel!
    
    @IBOutlet weak var dollarSignLabel: UILabel!
    
    
    @IBOutlet weak var segmentedControl: UISegmentedControl!
    
    @IBAction func segmentChanged(_ sender: Any) {
        switch segmentedControl.selectedSegmentIndex {
        case 0:
            self.containerViewBuyOrSell.alpha = 1
            self.containerViewBidOrAsk.alpha = 0
        case 1:
            self.containerViewBuyOrSell.alpha = 0
            self.containerViewBidOrAsk.alpha = 1
        default:
            break;
        }
    }
    
    @objc func keyboardWillShow(notification: NSNotification) {
        if segmentedControl.selectedSegmentIndex == 1 {
            if priceField.frame.origin.y == originPriceField {
                       priceField.frame.origin.y -= 216
                   }
                   if dollarSignLabel.frame.origin.y == dollarOrigin {
                       dollarSignLabel.frame.origin.y -= 216
                   }
        }
    }

    @objc func keyboardWillHide(notification: NSNotification) {
        if priceField.frame.origin.y != originPriceField {
            priceField.frame.origin.y = originPriceField!
        }
        if dollarSignLabel.frame.origin.y != dollarOrigin {
            dollarSignLabel.frame.origin.y = dollarOrigin!
            
        }
    }
    
    func textField(_ textField: UITextField, shouldChangeCharactersIn range: NSRange, replacementString string: String) -> Bool {
        //For mobile numer validation
        if textField == priceField {
            let allowedCharacters = CharacterSet(charactersIn:"+0123456789 ")//Here change this characters based on your requirement
            let characterSet = CharacterSet(charactersIn: string)
            return allowedCharacters.isSuperset(of: characterSet)
        }
        return true
    }
    
    @IBAction func didFinishEditingPrice(_ sender: Any) {
        var price = Int(priceField.text ?? "") ?? 0
        
        if (priceValue == nil) {
            return
        }
        
        // Buying
        if (isBuying! && segmentedControl.selectedSegmentIndex == 0) {
            if (price >= priceValue!) {
               priceField.text = String(priceValue!)
            } else {
                changeSegment(newPrice: price)
                priceField.becomeFirstResponder()
            }
        }
        
        // Bidding
        else if (isBuying! && segmentedControl.selectedSegmentIndex == 1) {
            if (price >= priceValue!) {
                changeSegment(newPrice: priceValue!)
            }
        }
        
        //Selling
        if (!isBuying! && segmentedControl.selectedSegmentIndex == 0) {
            if (price <= priceValue!) {
                priceField.text = String(priceValue!)
            } else {
                changeSegment(newPrice: price)
                priceField.becomeFirstResponder()
            }
        }
        
        // Asking
        else if (!isBuying! && segmentedControl.selectedSegmentIndex == 1) {
            if (price <= priceValue!) {
                changeSegment(newPrice: priceValue!)
            }
        }
    }
    
    func changeSegment(newPrice : Int) {
//        priceValue = newPrice
        
        priceField.text = "\(newPrice)"
        segmentedControl.selectedSegmentIndex = 1 - segmentedControl.selectedSegmentIndex
        segmentedControl.sendActions(for: UIControl.Event.valueChanged)
    }
    
    override func viewWillAppear(_ animated: Bool) {
        var endpoint = "\(NGROK_URL)/api/selling/get_bid/"
        if (isBuying!) {
            endpoint = "\(NGROK_URL)/api/buying/get_swipe/"
        }
        if (!matchAvailable!) {
            return
        }
        let parameters:[String: Any] = [
            "hall_id":hallId,
            "desired_price":Int(priceField.text!),
            "time_intervals": [
                [
                    "start":convertPickerTimeToJSONString(time:minimumTime!),
                    "end":convertPickerTimeToJSONString(time:maximumTime!)
                ]
            ]
        ]
//
//        hall_id (string): The dining hall identifier.
//        time_intervals (Datatime, optional): The desired time intervals. Defaults to None.
//        desired_price (Float, optional): The desired price. Defaults to None.
//        pair_type:
        
        AF.request(endpoint, method:.post, parameters: parameters, encoding:JSONEncoding.default).responseJSON { response in
            switch response.result {
                case .success:
                    if let value = response.value as? NSDictionary {
                        print(value)
//                        if let data = value.data(using: String.Encoding.utf8) {
//                            print(data)
//                        }
                        print(value["name"])
                        self.delegate?.gotSwipeInfo(info: value)
                        
                    }
                case let .failure(error):
                    print(error)
            }
            
            
        }
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
        
        originPriceField = priceField.frame.origin.y
        dollarOrigin = dollarSignLabel.frame.origin.y
        
        priceValue = isBuying! ? lowestAsk : highestBid
        
        priceField.text = "\(priceValue!)"
        
        if (priceValue == 0) {
            priceValue = nil
        }
        
        diningHallLabel.text = diningHallName
        diningHallLabel.adjustsFontSizeToFitWidth = true
        let font = UIFont.boldSystemFont(ofSize: 18)
        segmentedControl.frame.size.height = 50.0
        segmentedControl.setTitleTextAttributes([NSAttributedString.Key.font: font, NSAttributedString.Key.foregroundColor: #colorLiteral(red: 0.3332946301, green: 0.3333562613, blue: 0.333286047, alpha: 1)], for: .normal)
        segmentedControl.setTitleTextAttributes([NSAttributedString.Key.font: font, NSAttributedString.Key.foregroundColor:UIColor.white], for: .selected)
        
        segmentedControl.layer.cornerRadius = 30
        
        priceField.delegate = self
        
        
        NotificationCenter.default.addObserver(self, selector: #selector(self.keyboardWillShow), name: UIResponder.keyboardWillShowNotification, object: nil)
        NotificationCenter.default.addObserver(self, selector: #selector(self.keyboardWillHide), name: UIResponder.keyboardWillHideNotification, object: nil)
        
        if (isBuying!) {
            segmentedControl.setTitle("Buy", forSegmentAt:0)
            segmentedControl.setTitle("Bid", forSegmentAt:1)
            segmentedControl.selectedSegmentTintColor = #colorLiteral(red: 0.3411764801, green: 0.6235294342, blue: 0.1686274558, alpha: 1)
        } else {
            segmentedControl.setTitle("Sell", forSegmentAt:0)
            segmentedControl.setTitle("Ask", forSegmentAt:1)
            segmentedControl.selectedSegmentTintColor = #colorLiteral(red: 0.9379594326, green: 0.2973573804, blue: 0.3231473565, alpha: 1)
        }
        
        if (!matchAvailable!) {
            segmentedControl.setEnabled(false, forSegmentAt: 0)
            segmentedControl.selectedSegmentIndex=1;
        }
    }
    
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
            self.hidesBottomBarWhenPushed = true
            if (segue.identifier == "toBuyOrSellContainer")
            {
                let vc: BuyOrSellContainerVC = segue.destination as! BuyOrSellContainerVC
                vc.timePicker.minimumDate = minimumTime
                vc.timePicker.maximumDate = maximumTime
                vc.timePicker.date = minimumTime!
                vc.isBuying = isBuying
                vc.parentVC = self
                vc.hallId = hallId
                delegate = vc
            }
            if (segue.identifier == "toBidOrAskContainer")
                    {
                        let vc: BidOrAskContainerVC = segue.destination as! BidOrAskContainerVC
            //            vc.priceValue = priceValue!
                        vc.timePickerFrom.maximumDate = maximumTime!.addingTimeInterval(-15.0)
                        vc.timePickerTo.maximumDate = maximumTime
                       
                        vc.timePickerFrom.minimumDate = minimumTime
                        vc.timePickerTo.minimumDate = maximumTime!.addingTimeInterval(15.0)
                        vc.timePickerFrom.date = minimumTime!
                        vc.timePickerTo.date = maximumTime!
                        vc.isBidding = isBuying
                        vc.hallId = hallId
                        vc.parentVC = self
//                        bidOrAskContainerVC = vc
                        
                    }
        }

    override func viewDidAppear(_ animated: Bool) {
        super.viewDidAppear(animated)

        if (self.matchAvailable!) {
            UIView.animate(withDuration: 0.5, animations: {
                self.containerViewBuyOrSell.alpha = 1
                self.containerViewBidOrAsk.alpha = 0
            })
        }
        else {
            self.containerViewBidOrAsk.alpha = 1
            self.containerViewBuyOrSell.alpha = 0
        }
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
