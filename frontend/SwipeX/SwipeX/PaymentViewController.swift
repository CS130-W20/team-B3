//
//  PaymentViewController.swift
//  SwipeX
//
//  Created by Ashwin Vivek on 3/9/20.
//  Copyright © 2020 CS 130. All rights reserved.
//

import UIKit
import Stripe
import Alamofire
import SwiftyJSON

class PaymentViewController: UIViewController {

    var sellerName:String?
    var isBuying:Bool?
    var meetupTime:String?
    var price:String?
    var hallId:Int?
    var bidId:Int?
    @IBOutlet weak var sellerNameLabel: UILabel!
    
    var meetupTimeJSONString:String?
    
    @IBOutlet weak var priceLabel: UILabel!
    @IBOutlet weak var meetupTimeLabel: UILabel!
    @IBOutlet weak var cardTextField: STPPaymentCardTextField!
    
    var paymentIntentClientSecret: String?
    
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
        
        sellerNameLabel.text = sellerName
        meetupTimeLabel.text = meetupTime
        priceLabel.text = "$ \(price!)"
        
        startCheckout()
    }
    
    func displayAlert(title: String, message: String, restartDemo: Bool = false) {
        DispatchQueue.main.async {
            let alert = UIAlertController(title: title, message: message, preferredStyle: .alert)
            if restartDemo {
                alert.addAction(UIAlertAction(title: "Restart demo", style: .cancel) { _ in
                    self.cardTextField.clear()
                    self.startCheckout()
                })
            }
            else {
                alert.addAction(UIAlertAction(title: "OK", style: .cancel))
            }
            self.present(alert, animated: true, completion: nil)
        }
    }

    
    @IBAction func confirmPressed(_ sender: Any) {
        
        let cardParams = cardTextField.cardParams
               let paymentMethodParams = STPPaymentMethodParams(card: cardParams, billingDetails: nil, metadata: nil)
        let paymentIntentParams = STPPaymentIntentParams(clientSecret: paymentIntentClientSecret!)
        
        paymentIntentParams.paymentMethodParams = paymentMethodParams
        
        let paymentHandler = STPPaymentHandler.shared()
        
        let userId = UserDefaults.standard.integer(forKey: "userId")
        let parameters = [
            "user_id": userId,
            "hall_id": hallId,
            "swipe_id": bidId,
            "desired_price": price,
            "desired_time": meetupTimeJSONString
            ] as [String : Any]
        
        paymentHandler.confirmPayment(withParams: paymentIntentParams, authenticationContext: self) { (status, paymentIntent, error) in
            switch (status) {
            case .failed:
                self.displayAlert(title: "Payment failed", message: error?.localizedDescription ?? "")
                break
            case .canceled:
                self.displayAlert(title: "Payment canceled", message: error?.localizedDescription ?? "")
                break
            case .succeeded:
                AF.request("\(NGROK_URL)/api/buying/buy/", method:.post, parameters: parameters, encoding:JSONEncoding.default).responseJSON { response in
                    switch response.result {
                        case .success:
                            if let value = response.value as? NSDictionary {
                                print(value)
                                self.dismiss(animated: true, completion: nil)
                            }
                        case let .failure(error):
                            print(error)
                    }
                }
                break
            @unknown default:
                fatalError()
                break
            }
        }

    }
    
    func startCheckout() {
        // Create a PaymentIntent by calling the sample server's /create-payment-intent endpoint.
        let url = URL(string: NGROK_URL + "/api/pay/ask/")!
        
        print(price)
        let parameters: [String: Any] = [
            "amount": (Int(price!)!*100)
        ]
        
        AF.request(url, method:.post, parameters: parameters, encoding:JSONEncoding.default).responseJSON { response in
            switch response.result {
                case .success:
                    print(response.value)
                    if let value = response.value as? String {
                        if let data = value.data(using: String.Encoding.utf8) {
                            let json = JSON(data)
                            print(json)
                            print(json["client_secret"])
                            
                            self.paymentIntentClientSecret = json["client_secret"].stringValue
                            
                            Stripe.setDefaultPublishableKey("pk_test_d3JzWCczi1nb43jv9y1Kpvrg00XSfsIYXE")
                        }
                    }
                case let .failure(error):
                    print(error)
            }
        }
//        
//        var request = URLRequest(url: url)
//        request.httpMethod = "POST"
//        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
//        request.httpBody = try? JSONSerialization.data(withJSONObject: json)
//        let task = URLSession.shared.dataTask(with: request, completionHandler: { [weak self] (data, response, error) in
//            guard let response = response as? HTTPURLResponse,
//                response.statusCode == 200,
//                let data = data,
//                let json = try? JSONSerialization.jsonObject(with: data, options: []) as? [String : Any],
//                let clientSecret = json["clientSecret"] as? String,
//                let publishableKey = json["publishableKey"] as? String else {
//                    let message = error?.localizedDescription ?? "Failed to decode response from server."
//                    self?.displayAlert(title: "Error loading page", message: message)
//                    return
//            }
//            print("Created PaymentIntent")
//            self?.paymentIntentClientSecret = clientSecret
//            // Configure the SDK with your Stripe publishable key so that it can make requests to the Stripe API
//            // For added security, our sample app gets the publishable key from the server
//            Stripe.setDefaultPublishableKey(publishableKey)
//        })
//        task.resume()
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

extension PaymentViewController: STPAuthenticationContext {
    func authenticationPresentingViewController() -> UIViewController {
        return self
    }
}
