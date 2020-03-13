//
//  SwipeSummaryViewController.swift
//  SwipeX
//
//  Created by Ashwin Vivek on 3/12/20.
//  Copyright © 2020 CS 130. All rights reserved.
//

import UIKit
import Alamofire
import SwiftyJSON

class SwipeSummaryViewController: UIViewController, UITableViewDelegate, UITableViewDataSource {
    
    @IBOutlet weak var acceptedBids: UITableView!
    @IBOutlet weak var acceptedAsks: UITableView!
    @IBOutlet weak var pendingBids: UITableView!
    @IBOutlet weak var pendingAsks: UITableView!
    
    var acceptedBidsArray = [NSDictionary]()
    var acceptedSwipesArray = [NSDictionary]()
    var pendingBidsArray = [NSDictionary]()
    var pendingSwipesArray = [NSDictionary]()
    
    override func viewWillAppear(_ animated: Bool) {
        let userId = UserDefaults.standard.integer(forKey: "userId")
               let parameters = [
                   "user_id": userId
               ]
               AF.request("\(NGROK_URL)/api/accounts/user_data/", method:.post, parameters: parameters, encoding:JSONEncoding.default).responseJSON { response in
                   switch response.result {
                       case .success:
                           if let value = response.value as? NSDictionary {
                            let bidsDict = value["Bids"] as? NSDictionary
                            let swipesDict = value["Swipes"] as? NSDictionary
                            
                            self.acceptedBidsArray = bidsDict!["Accepted"] as! [NSDictionary]
                            
                            self.pendingBidsArray = bidsDict!["Pending"] as! [NSDictionary]
                            self.acceptedSwipesArray = swipesDict!["Sold"] as! [NSDictionary]
                            self.pendingSwipesArray = swipesDict!["Available"] as! [NSDictionary]
                            
                            print(self.pendingBidsArray)
                           }
                       case let .failure(error):
                           print(error)
                   }
               }
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
        acceptedAsks.delegate = self
        acceptedAsks.dataSource = self
        acceptedBids.delegate = self
        acceptedBids.dataSource = self
        pendingAsks.delegate = self
        pendingAsks.dataSource = self
        pendingBids.delegate = self
        pendingBids.dataSource = self
    }
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        if(tableView == self.acceptedAsks) {
            return acceptedSwipesArray.count
        }
        else if(tableView == self.acceptedBids) {
            return acceptedBidsArray.count
        }
        else if(tableView == self.pendingAsks) {
            return pendingSwipesArray.count
        }
        else if(tableView == self.pendingBids) {
            return pendingBidsArray.count
        }
        return 1
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "informationCell", for: indexPath) as! informationCell
        
        print(self.pendingBids)
        print(self.pendingAsks)
        return cell
        if(tableView == self.acceptedAsks) {
//            cell.name =
        }
        else if(tableView == self.acceptedBids) {
        }
        else if(tableView == self.pendingAsks) {
        }
        else if(tableView == self.pendingBids) {
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
