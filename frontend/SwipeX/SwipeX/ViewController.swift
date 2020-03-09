//
//  ViewController.swift
//  SwipeX
//
//  Created by Ashwin Vivek on 3/3/20.
//  Copyright © 2020 CS 130. All rights reserved.
//

import UIKit
import Alamofire
import SwiftyJSON

class ViewController: UIViewController, UICollectionViewDataSource, UICollectionViewDelegate, UICollectionViewDelegateFlowLayout {

    @IBOutlet weak var diningHallCollection: UICollectionView!
    @IBOutlet weak var quickServiceCollection: UICollectionView!
    
    var halls:[JSON] = []
    var quicks:[JSON] = []
    
    let diningHalls = ["BPlate", "De Neve", "Feast", "Covel"]
    let quickService = ["Cafe 1919", "The Study at Hedrick", "Rendezvous", "BCafe"]
    
    var selectedDiningHallIndex: Int = 0
    var didSelectDiningHall: Bool = true
    
    func convertTime(jsonTime: JSON) -> String{
        var start = Int(jsonTime["start"].stringValue)!
        var end = Int(jsonTime["end"].stringValue)!
        
        if (start == 0 && end == 0) {
            return "closed"
        }
        
        var start_am_or_pm = "am"
        var end_am_or_pm = "am"
        if (start > 12) {
            start = start - 12
            start_am_or_pm = "pm"
        }
        if (end > 12) {
            end = end - 12
            end_am_or_pm = "pm"
        }
        return "\(start)\(start_am_or_pm) - \(end)\(end_am_or_pm)"
    }
    
    func convertTimeForPicker(time: Int) -> String{
        var am_or_pm = (time >= 12) ? "pm" : "am"
        
        return "\(time > 12 ? time - 12 : time):00 \(am_or_pm)"
    }
    
    func collectionView(_ collectionView: UICollectionView, numberOfItemsInSection section: Int) -> Int {
        if(collectionView == self.diningHallCollection) {
            return diningHalls.count
        }
        else if (collectionView == self.quickServiceCollection) {
            return quickService.count
        }
        return 0
    }
    
    func collectionView(_ collectionView: UICollectionView,
    layout collectionViewLayout: UICollectionViewLayout,
    sizeForItemAt indexPath: IndexPath) -> CGSize {
        return CGSize(width: 342, height: 226);
    }
    
    func collectionView(_ collectionView: UICollectionView, layout collectionViewLayout: UICollectionViewLayout, insetForSectionAt section: Int) -> UIEdgeInsets {
        return UIEdgeInsets(top: 0, left: 5, bottom: 0, right: 5)
    }
    func collectionView(_ collectionView: UICollectionView, cellForItemAt indexPath: IndexPath) -> UICollectionViewCell {
        let cell = collectionView.dequeueReusableCell(withReuseIdentifier: "Cell", for: indexPath) as! diningHallCell
        if(collectionView == self.diningHallCollection) {
            let arrayEmpty = quicks.isEmpty
            
            if (arrayEmpty) {
                let activityView = UIActivityIndicatorView(style: .gray)
                activityView.center = CGPoint(x: cell.contentView.frame.size.width / 2, y: cell.contentView.frame.size.height / 2)
                
                cell.lowestAsk.isHidden = true
                cell.image.isHidden = true
                cell.numBids.isHidden = true
                cell.timesAvailable.isHidden = true
                cell.name.isHidden = true
                
                cell.contentView.addSubview(activityView)
                activityView.startAnimating()
            }
            else {
                cell.lowestAsk.isHidden = false
                cell.image.isHidden = false
                cell.numBids.isHidden = false
                cell.timesAvailable.isHidden = false
                cell.name.isHidden = false
                cell.name.text = halls.isEmpty ? "" : "\(halls[indexPath.row]["name"])"
                cell.image.image = arrayEmpty ? UIImage(named: "feast") : UIImage(named: "\(halls[indexPath.row]["name"])".lowercased())
                cell.numBids.text = halls.isEmpty ? "" :
                    "\(halls[indexPath.row]["nBids"]) bids"
                
                let lowestAsk = arrayEmpty ? 0 : halls[indexPath.row]["lowest_ask"]
                cell.lowestAsk.text = (arrayEmpty || lowestAsk.intValue == 0) ? "0 asks" : "$\(halls[indexPath.row]["lowest_ask"]) lowest ask"
                
                cell.timesAvailable.text = arrayEmpty ? "Closed" : convertTime(jsonTime: halls[indexPath.row]["times"])
            }
        }
        else if (collectionView == self.quickServiceCollection) {
            let arrayEmpty = quicks.isEmpty
            if (arrayEmpty) {
                let activityView = UIActivityIndicatorView(style: .gray)
                activityView.center = CGPoint(x: cell.contentView.frame.size.width / 2, y: cell.contentView.frame.size.height / 2)
                
                cell.lowestAsk.isHidden = true
                cell.image.isHidden = true
                cell.numBids.isHidden = true
                cell.timesAvailable.isHidden = true
                cell.name.isHidden = true
            
                cell.contentView.addSubview(activityView)
                activityView.startAnimating()
            } else {
                cell.lowestAsk.isHidden = false
                cell.image.isHidden = false
                cell.numBids.isHidden = false
                cell.timesAvailable.isHidden = false
                cell.name.isHidden = false
                
                cell.name.text = arrayEmpty ? "" : "\(quicks[indexPath.row]["name"])"
                
                cell.image.image = arrayEmpty ? UIImage(named: "feast") : UIImage(named: "\(quicks[indexPath.row]["name"])".lowercased())
                
                cell.numBids.text = arrayEmpty ? "" : "\(quicks[indexPath.row]["nBids"]) bids"

                let lowestAsk = arrayEmpty ? 0 : halls[indexPath.row]["lowest_ask"]
                
                cell.lowestAsk.text = (arrayEmpty || lowestAsk.intValue == 0) ? "0 asks" : "$\(quicks[indexPath.row]["lowest_ask"]) lowest ask"
                
                cell.timesAvailable.text = arrayEmpty ? "Closed" : convertTime(jsonTime: quicks[indexPath.row]["times"])
            }
        }
        cell.image.contentMode = UIView.ContentMode.scaleAspectFill
        cell.layer.borderColor = UIColor.lightGray.cgColor
        cell.layer.borderWidth = 0.1
        cell.layer.shadowColor = UIColor.lightGray.cgColor
        cell.layer.shadowOffset = CGSize(width: 0, height: 6.0)
        cell.layer.shadowRadius = 10
        cell.layer.shadowOpacity = 0.5
        cell.layer.masksToBounds = false
        
        cell.lowestAsk.adjustsFontSizeToFitWidth = true
        
        collectionView.layer.masksToBounds = false
        return cell
    }
    
    
    func collectionView(_ collectionView: UICollectionView, didSelectItemAt indexPath: IndexPath) {
        selectedDiningHallIndex = indexPath.row
        if (collectionView == self.diningHallCollection) {
            didSelectDiningHall = true
        } else {
            didSelectDiningHall = false
        }
        self.performSegue(withIdentifier: "diningHallsToSwipePrice", sender: self)
    }
    
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        if (segue.identifier == "diningHallsToSwipePrice") {
            // pass data to next view
            if let destinationVC = segue.destination as? SwipePriceViewController {
                if (didSelectDiningHall) {
                    destinationVC.diningHallName = halls[selectedDiningHallIndex]["name"].stringValue
                    destinationVC.lowestAsk = halls[selectedDiningHallIndex]["lowest_ask"].intValue
                    
                    // TODO
                    destinationVC.highestBid = 5
                    
                    destinationVC.numAsks = halls[selectedDiningHallIndex]["nSwipes"].intValue
                    destinationVC.numBids = halls[selectedDiningHallIndex]["nBids"].intValue
                    
                    destinationVC.minTime = convertTimeForPicker(time: halls[selectedDiningHallIndex]["times"]["start"].intValue)
                    destinationVC.maxTime = convertTimeForPicker(time: halls[selectedDiningHallIndex]["times"]["end"].intValue)
                    destinationVC.hallId = halls[selectedDiningHallIndex]["hall_id"].intValue
                    
                } else {
                    destinationVC.diningHallName = quicks[selectedDiningHallIndex]["name"].stringValue
                    destinationVC.lowestAsk = quicks[selectedDiningHallIndex]["lowest_ask"].intValue
                    
                    destinationVC.highestBid = 5
                    
                    destinationVC.numAsks = quicks[selectedDiningHallIndex]["nSwipes"].intValue
                    destinationVC.numBids = quicks[selectedDiningHallIndex]["nBids"].intValue
                    destinationVC.minTime = convertTimeForPicker(time: quicks[selectedDiningHallIndex]["times"]["start"].intValue)
                    destinationVC.maxTime = convertTimeForPicker(time: quicks[selectedDiningHallIndex]["times"]["end"].intValue)
                    destinationVC.hallId = quicks[selectedDiningHallIndex]["hall_id"].intValue
                }
            }
        }
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
        quickServiceCollection.delegate = self
        quickServiceCollection.dataSource = self
        
        diningHallCollection.delegate = self
        diningHallCollection.dataSource = self
          
        AF.request("https://822f9117.ngrok.io/api/swipes/homescreen_info/", method:.get).responseJSON { response in
            switch response.result {
            case .success:
                if let value = response.value as? String {
                    if let data = value.data(using: String.Encoding.utf8) {
                        let json = JSON(data)
                        print(json)
                        if let quickService =  json["quick"].arrayValue as [JSON]? {
                            self.quicks = quickService
                            print(self.quicks)
                            self.quickServiceCollection.reloadData()
                        }
                        if let dining =  json["halls"].arrayValue as [JSON]? {
                            self.halls = dining
                            print(self.halls)
                            self.diningHallCollection.reloadData()
                        }
                    }
                }
            case let .failure(error):
                print(error)
            }
        }
    }
}

