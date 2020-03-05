//
//  SwipePriceViewController.swift
//  SwipeX
//
//  Created by Ashwin Vivek on 2/19/20.
//  Copyright © 2020 CS 130. All rights reserved.
//

import UIKit

class SwipePriceViewController: UIViewController{
    var diningHallName : String?
    var lowestAsk : Int?
    var highestBid: Int?
    
    @IBOutlet weak var fromTime: UITextField!
    @IBOutlet weak var toTime: UITextField!

    @IBOutlet weak var lowestAskLabel: UILabel!
    @IBOutlet weak var highestBidLabel: UILabel!
    @IBOutlet weak var diningHallLabel: UILabel!
    
    @IBOutlet weak var lowestAskView: UIView!
    @IBOutlet weak var highestBidView: UIView!
    
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
            if (didTapBuy!) {
                vc.priceValue = lowestAsk
            } else {
                vc.priceValue = highestBid
            }
        }
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        diningHallLabel.text = diningHallName
        lowestAskLabel.text = "$\(lowestAsk!)"
        highestBidLabel.text = "$\(highestBid!)"
        
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
        self.datePickerFrom.minimumDate =  timeFormatter.date(from: "5:00 pm")
        self.datePickerFrom.maximumDate =  timeFormatter.date(from: "7:30 pm")
        self.datePickerFrom.date = timeFormatter.date(from: "5:00 pm")!
        
        fromTime.text = timeFormatter.string(from: timeFormatter.date(from: "5:00 pm")!)

        self.toTime.inputView = self.datePickerTo
        self.toTime.inputAccessoryView = self.datePickerFrom.toolbar
        self.datePickerTo.datePickerMode = UIDatePicker.Mode.time
        self.datePickerTo.minuteInterval = 30
        self.datePickerTo.toolbarDelegate = self
        self.datePickerTo.minimumDate =  timeFormatter.date(from: "5:30 pm")
        self.datePickerTo.maximumDate =  timeFormatter.date(from: "8:00 pm")
        self.datePickerTo.date = timeFormatter.date(from: "8:00 pm")!
        
        toTime.text = timeFormatter.string(from: timeFormatter.date(from: "8:00 pm")!)
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
        // TODO: Filter the best ask and bid
    }
    
    func didTapCancel() {
        if(self.didTapFrom!) {
            self.fromTime.resignFirstResponder()
        } else {
            self.toTime.resignFirstResponder()
        }
    }
}
