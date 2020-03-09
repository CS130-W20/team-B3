//
//  BuyOrSellContainerVC.swift
//  SwipeX_2
//
//  Created by Ashwin Vivek on 2/20/20.
//  Copyright © 2020 CS 130. All rights reserved.
//

import UIKit

class BuyOrSellContainerVC: UIViewController, UITextFieldDelegate {
    
    weak var parentVC: BuyOrSellViewController?
    
    @IBOutlet weak var OneSwipeLabel: UILabel!

    @IBOutlet weak var priceField: UITextField!
    var priceValue:Int!
    @IBOutlet weak var timeField: UITextField!

    
    @IBOutlet weak var infoHeaderLabel: UILabel!
    
    @IBOutlet weak var actionButton: UIButton!
    @IBOutlet weak var sellerInfoView: UIView!
    
    @IBOutlet weak var infoPersonNameLabel: UILabel!
    @IBOutlet weak var infoRatingLabel: UILabel!
    var timePicker = ToolbarDatePicker()
    
    var isBuying:Bool!
    var hallId:Int!
    
    @IBAction func didFinishEditingPrice(_ sender: Any) {
        var price = Int(priceField.text ?? "") ?? 0
        if (price < priceValue!) {
            parentVC?.changeSegment(newPrice: price)
        }
    }
    
//
    
    
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
        
        self.hideKeyboardWhenTappedAround()
        if (isBuying) {
            OneSwipeLabel.text = "Buy one swipe for..."
            actionButton.setTitle("Buy Now", for: .normal)
            actionButton.backgroundColor = #colorLiteral(red: 0.3411764801, green: 0.6235294342, blue: 0.1686274558, alpha: 1)
            infoHeaderLabel.text = "Seller Info"
        } else {
            OneSwipeLabel.text = "Sell one swipe for..."
            actionButton.setTitle("Sell Now", for: .normal)
            infoHeaderLabel.text = "Buyer Info"
            actionButton.backgroundColor = #colorLiteral(red: 0.9379594326, green: 0.2973573804, blue: 0.3231473565, alpha: 1)
        }
        
        sellerInfoView.layer.shadowColor = UIColor.lightGray.cgColor
        sellerInfoView.layer.shadowOpacity = 0.5
        sellerInfoView.layer.shadowOffset = CGSize(width: 0, height: 6.0)
        sellerInfoView.layer.shadowRadius = 3
        sellerInfoView.layer.cornerRadius = 15
        
        timePicker.datePickerMode = UIDatePicker.Mode.time
        timePicker.minuteInterval = 15
        timePicker.toolbarDelegate = self
        
        priceField.text = "\(priceValue!)"
        
        var timeFormatter = DateFormatter()
        timeFormatter.dateStyle = DateFormatter.Style.none
        timeFormatter.timeStyle = DateFormatter.Style.short
        
        self.timeField.text = timeFormatter.string(from: timePicker.minimumDate!)
        self.timeField.inputView = self.timePicker
        self.timeField.inputAccessoryView = self.timePicker.toolbar
        
        self.priceField.delegate = self
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
    

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destination.
        // Pass the selected object to the new view controller.
    }
    */

}

extension BuyOrSellContainerVC: ToolbarDatePickerDelegate {

    func didTapDone() {
        let timeFormatter = DateFormatter()
        timeFormatter.dateStyle = DateFormatter.Style.none
        timeFormatter.timeStyle = DateFormatter.Style.short
        
        timeField.text = timeFormatter.string(from: self.timePicker.date)
        self.timeField.resignFirstResponder()
    }
    
    func didTapCancel() {
        self.timeField.resignFirstResponder()
    }
}
