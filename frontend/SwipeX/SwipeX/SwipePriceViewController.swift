//
//  SwipePriceViewController.swift
//  SwipeX
//
//  Created by Ashwin Vivek on 2/19/20.
//  Copyright © 2020 CS 130. All rights reserved.
//

import UIKit
import Alamofire
import SwiftyJSON

class SwipePriceViewController: UIViewController{
    var diningHallName : String?
    var lowestAsk : Int?
    var highestBid: Int?
    var hallId: Int?
    
    @IBOutlet weak var askImage: UIImageView!
    @IBOutlet weak var bidImage: UIImageView!
    var numAsks: Int?
    var numBids: Int?
    
    @IBOutlet weak var fromTime: UITextField!
    @IBOutlet weak var toTime: UITextField!
    
    var minTimeString: String?
    var maxTimeString: String?
    var minTimeInt:Int?
    var maxTimeInt:Int?
    
    var intervals:JSON!

    @IBOutlet weak var lowestAskLabel: UILabel!
    @IBOutlet weak var highestBidLabel: UILabel!
    @IBOutlet weak var diningHallLabel: UILabel!
    
    @IBOutlet weak var lowestAskView: UIView!
    @IBOutlet weak var highestBidView: UIView!
    
    @IBOutlet weak var numSellingLabel: UILabel!
    @IBOutlet weak var numBuyingLabel: UILabel!
    
    var didTapFrom: Bool?
    var didTapBuy:Bool?
    
    @IBAction func didTapFrom(_ sender: Any) {
          didTapFrom = true
    }
    @IBAction func didTapTo(_ sender: Any) {
          didTapFrom = false
    }
    fileprivate let datePickerFrom = ToolbarDatePicker()
    fileprivate let datePickerTo = ToolbarDatePicker()
    
    @IBAction func didTapBuyButton(_ sender: Any) {
        didTapBuy = true
        self.performSegue(withIdentifier: "SwipePriceToBuyOrSell", sender: self)
    }
    
    @IBAction func didTapSellButton(_ sender: Any) {
        didTapBuy = false
        self.performSegue(withIdentifier: "SwipePriceToBuyOrSell", sender: self)
    }
    
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        if (segue.identifier == "SwipePriceToBuyOrSell") {
            let vc: BuyOrSellViewController = segue.destination as! BuyOrSellViewController
            vc.isBuying = didTapBuy
            vc.diningHallName = diningHallName
            if (didTapBuy!) {
                vc.priceValue = lowestAsk
                vc.matchAvailable = numAsks! > 0
            } else {
                vc.priceValue = highestBid
                vc.matchAvailable = numBids! > 0
            }
            
            vc.minimumTime = self.datePickerFrom.date
            vc.maximumTime = self.datePickerTo.date
            vc.hallId = hallId
        }
    }

    override func viewWillAppear(_ animated: Bool) {
        let parameters:[String: Any] = [
                "hall_id": hallId,
                "start": minTimeInt,
                "end": maxTimeInt,
            ]
        
        AF.request("\(NGROK_URL)/api/swipes/timeinterval_info/", method:.post, parameters: parameters, encoding:JSONEncoding.default).responseJSON { response in
                    switch response.result {
                        case .success:
                            if let value = response.value as? String {
                                if let data = value.data(using: String.Encoding.utf8) {
                                    self.intervals = JSON(data)
                                    
                                    print(self.intervals!)
                                    print(self.minTimeInt)
                                    print(self.intervals!["\(self.minTimeInt!)"])
                                    
                                    self.lowestAskLabel.text = "$\(self.intervals!["\(self.minTimeInt!)"]["\(self.maxTimeInt!)"]["swipe"])"
                                    self.highestBidLabel.text = "$\(self.intervals!["\(self.minTimeInt!)"]["\(self.maxTimeInt!)"]["bid"])"
                                }
                            }
                        case let .failure(error):
                            print(error)
                    }
                }
    }
    
    func updateBidAndAskLabels(begin:Int, end: Int) {
        
        let la = self.intervals!["\(begin)"]["\(end)"]["swipe"]
        let hb = self.intervals!["\(begin)"]["\(end)"]["bid"]
        
        self.lowestAskLabel.text = "$\(la.intValue)"
        self.highestBidLabel.text = "$\(hb.intValue)"
        
        self.lowestAsk = la.intValue
        self.highestBid = hb.intValue
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        diningHallLabel.text = diningHallName
        diningHallLabel.adjustsFontSizeToFitWidth = true
        diningHallLabel.baselineAdjustment = .alignCenters
        
        numSellingLabel.text = "\(numAsks!) selling"
        numBuyingLabel.text = "\(numBids!) buying"
        
        if (numAsks! > 0) {
            lowestAskLabel.isHidden = false
        } else {
            askImage.image = UIImage(named: "noAsks")
            lowestAskLabel.isHidden = true
        }
        
        if (numBids! > 0) {
            highestBidLabel.isHidden = false
        } else {
            bidImage.image = UIImage(named: "noBids")
            highestBidLabel.isHidden = true
        }
        
        lowestAskView.layer.shadowColor = UIColor.lightGray.cgColor
        lowestAskView.layer.shadowOpacity = 0.5
        lowestAskView.layer.shadowOffset = CGSize(width: 0, height: 6.0)
        lowestAskView.layer.shadowRadius = 3
        lowestAskView.layer.cornerRadius = 15
        
        highestBidView.layer.shadowColor = UIColor.lightGray.cgColor
        highestBidView.layer.shadowOpacity = 0.5
        highestBidView.layer.shadowOffset = CGSize(width: 0, height: 6.0)
        highestBidView.layer.shadowRadius = 3
        highestBidView.layer.cornerRadius = 15
        lowestAskLabel.adjustsFontSizeToFitWidth = true
        highestBidLabel.adjustsFontSizeToFitWidth = true
        // Do any additional setup after loading the view.
        var timeFormatter = DateFormatter()
        timeFormatter.dateStyle = DateFormatter.Style.none
        timeFormatter.timeStyle = DateFormatter.Style.short
        self.title = diningHallName
        
        self.fromTime.inputView = self.datePickerFrom
        self.fromTime.inputAccessoryView = self.datePickerFrom.toolbar
        self.datePickerFrom.datePickerMode = UIDatePicker.Mode.time
        self.datePickerFrom.minuteInterval = 30
        self.datePickerFrom.toolbarDelegate = self
        self.datePickerFrom.minimumDate =  timeFormatter.date(from: minTimeString!)
//        self.datePickerFrom.maximumDate =  timeFormatter.date(from: "7:30 pm")
        self.datePickerFrom.date = timeFormatter.date(from: minTimeString!)!
        
        self.datePickerFrom.maximumDate =  self.datePickerTo.date.addingTimeInterval(-30.0)
        
        fromTime.text = timeFormatter.string(from: timeFormatter.date(from: minTimeString!)!)

        self.toTime.inputView = self.datePickerTo
        self.toTime.inputAccessoryView = self.datePickerFrom.toolbar
        self.datePickerTo.datePickerMode = UIDatePicker.Mode.time
        self.datePickerTo.minuteInterval = 30
        self.datePickerTo.toolbarDelegate = self
        self.datePickerTo.maximumDate =  timeFormatter.date(from: maxTimeString!)
        self.datePickerTo.date = timeFormatter.date(from: maxTimeString!)!
        self.datePickerTo.minimumDate =  self.datePickerFrom.date.addingTimeInterval(30.0)
        
        toTime.text = timeFormatter.string(from: timeFormatter.date(from: maxTimeString!)!)
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

extension SwipePriceViewController: ToolbarDatePickerDelegate {

    func didTapDone() {
        var timeFormatter = DateFormatter()
        timeFormatter.dateStyle = DateFormatter.Style.none
        timeFormatter.timeStyle = DateFormatter.Style.short
        
        if (self.didTapFrom!) {
            fromTime.text = timeFormatter.string(from: self.datePickerFrom.date)
            self.datePickerTo.minimumDate = self.datePickerFrom.date.addingTimeInterval(30.0)
            self.fromTime.resignFirstResponder()
        } else {
            toTime.text = timeFormatter.string(from: self.datePickerTo.date)
            self.datePickerFrom.maximumDate = self.datePickerTo.date.addingTimeInterval(-30.0)
            self.toTime.resignFirstResponder()
        }
        // TODO: Filter the best ask and bi
        
        updateBidAndAskLabels(begin: convertPickerTimeToInt(time: self.datePickerFrom.date), end: convertPickerTimeToInt(time: self.datePickerTo.date))
        
    }
    
    func didTapCancel() {
        if(self.didTapFrom!) {
            self.fromTime.resignFirstResponder()
        } else {
            self.toTime.resignFirstResponder()
        }
    }
}
