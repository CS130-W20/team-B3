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
        
        fromTime.text = timeFormatter.string(from: timeFormatter.date(from: "5:00 pm")!)

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
