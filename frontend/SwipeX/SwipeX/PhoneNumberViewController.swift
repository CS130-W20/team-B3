//
//  PhoneNumberViewController.swift
//  SwipeX
//
//  Created by Ashwin Vivek on 3/8/20.
//  Copyright © 2020 CS 130. All rights reserved.
//

import UIKit
import PhoneNumberKit
import Alamofire

class PhoneNumberViewController: UIViewController, UITextFieldDelegate {

    @IBOutlet weak var phoneNumberField: PhoneNumberTextField!
    let phoneNumberKit = PhoneNumberKit()
    
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
        
        var bottomLine = CALayer()
        bottomLine.frame = CGRect(x: 0.0, y: phoneNumberField.frame.height - 1, width: phoneNumberField.frame.width, height: 1.0)
        bottomLine.backgroundColor = UIColor.white.cgColor
        phoneNumberField.borderStyle = UITextField.BorderStyle.none
        phoneNumberField.layer.addSublayer(bottomLine)
        
        phoneNumberField.delegate = self
        
        
    }
    
    @IBAction func signUpPressed(_ sender: Any) {
        
        let name = UserDefaults.standard.string(forKey: "fullName")
        let email = UserDefaults.standard.string(forKey: "email")
        let parameters: [String: String] = [
            "phone": phoneNumberField.text!,
            "name": name!,
            "email": email!
        ]
    AF.request("https://d7d02573.ngrok.io/api/accounts/create/", method: .post, parameters: parameters, encoder: JSONParameterEncoder.default).responseJSON { response in
            switch response.result {
            case .success:
                print("YES")
            case let .failure(error):
                print(error)
            }
        }
    }
    
    func textField(_ textField: UITextField, shouldChangeCharactersIn range: NSRange, replacementString string: String) -> Bool {

        let maxLength = 14
        let currentString: NSString = phoneNumberField.text! as NSString
        let newString: NSString = currentString.replacingCharacters(in: range, with: string) as NSString

        if newString.length == maxLength {
            phoneNumberField.text = textField.text! + string
            phoneNumberField.resignFirstResponder()
        }

        return newString.length <= maxLength
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
