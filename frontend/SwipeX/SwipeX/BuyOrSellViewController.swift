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
    
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
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
    }

    override func viewDidAppear(_ animated: Bool) {
        super.viewDidAppear(animated)

        UIView.animate(withDuration: 0.5, animations: {
                self.containerViewBuyOrSell.alpha = 1
                self.containerViewBidOrAsk.alpha = 0
            })
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
