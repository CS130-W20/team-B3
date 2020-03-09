//
//  BuyOrSellViewController.swift
//  SwipeX_2
//
//  Created by Ashwin Vivek on 2/20/20.
//  Copyright © 2020 CS 130. All rights reserved.
//

import UIKit

class BuyOrSellViewController: UIViewController {

    @IBOutlet weak var containerViewBuyOrSell: UIView!
    @IBOutlet weak var containerViewBidOrAsk: UIView!
    
    var isBuying:Bool?
    var priceValue:Int?
    let timePicker = ToolbarDatePicker()
    var minimumTime:Date?
    var maximumTime:Date?
    var matchAvailable:Bool?
    var diningHallName:String?
    var hallId:Int?
    
    @IBOutlet weak var diningHallLabel: UILabel!
    
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
    
    func changeSegment(newPrice : Int) {
        priceValue = newPrice
        
        segmentedControl.selectedSegmentIndex = 1 - segmentedControl.selectedSegmentIndex
        segmentedControl.sendActions(for: UIControl.Event.valueChanged)
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
        diningHallLabel.text = diningHallName
        diningHallLabel.adjustsFontSizeToFitWidth = true
        let font = UIFont.boldSystemFont(ofSize: 18)
        segmentedControl.frame.size.height = 50.0
        segmentedControl.setTitleTextAttributes([NSAttributedString.Key.font: font, NSAttributedString.Key.foregroundColor: #colorLiteral(red: 0.3332946301, green: 0.3333562613, blue: 0.333286047, alpha: 1)], for: .normal)
        segmentedControl.setTitleTextAttributes([NSAttributedString.Key.font: font, NSAttributedString.Key.foregroundColor:UIColor.white], for: .selected)
        
        segmentedControl.layer.cornerRadius = 30
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
                vc.priceValue = priceValue!
                vc.timePicker.minimumDate = minimumTime
                vc.timePicker.maximumDate = maximumTime
                vc.timePicker.date = minimumTime!
                vc.isBuying = isBuying
                vc.parentVC = self
                vc.hallId = hallId
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
                        vc.priceValue = priceValue
                        vc.isBidding = isBuying
                        vc.hallId = hallId
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
