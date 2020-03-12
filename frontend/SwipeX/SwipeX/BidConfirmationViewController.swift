//
//  BidConfirmationViewController.swift
//  SwipeX
//
//  Created by Ashwin Vivek on 3/11/20.
//  Copyright © 2020 CS 130. All rights reserved.
//

import UIKit

class BidConfirmationViewController: UIViewController {

    var price:Int?
    var meetupTimeString:String?
    @IBOutlet weak var priceLabel: UILabel!
    @IBOutlet weak var meetupTimes: UILabel!
    
    @IBAction func confirmPressed(_ sender: Any) {
//        self.navigationController.
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
