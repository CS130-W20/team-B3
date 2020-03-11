//
//  PaymentViewController.swift
//  SwipeX
//
//  Created by Ashwin Vivek on 3/9/20.
//  Copyright © 2020 CS 130. All rights reserved.
//

import UIKit
import Stripe

class PaymentViewController: UIViewController {

    var sellerName:String?
    var isBuying:Bool?
    var meetupTime:String?
    var price:String?
    @IBOutlet weak var sellerNameLabel: UILabel!
    
    @IBOutlet weak var priceLabel: UILabel!
    @IBOutlet weak var meetupTimeLabel: UILabel!
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
        
        sellerNameLabel.text = sellerName
        meetupTimeLabel.text = meetupTime
        priceLabel.text = "$ \(price!)"
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
