//
//  SwipePriceViewController.swift
//  SwipeX_2
//
//  Created by Ashwin Vivek on 2/19/20.
//  Copyright © 2020 CS 130. All rights reserved.
//

import UIKit

protocol ToolbarDatePickerDelegate: class {
    func didTapDone()
    func didTapCancel()
}

class ToolbarDatePicker: UIDatePicker {

    public private(set) var toolbar: UIToolbar?
    public weak var toolbarDelegate: ToolbarDatePickerDelegate?

    override init(frame: CGRect) {
        super.init(frame: frame)
        self.commonInit()
    }

    required init?(coder aDecoder: NSCoder) {
        super.init(coder: aDecoder)
        self.commonInit()
    }

    private func commonInit() {
        let toolBar = UIToolbar()
        toolBar.barStyle = UIBarStyle.default
        toolBar.isTranslucent = true
        toolBar.tintColor = .black
        toolBar.sizeToFit()

        let doneButton = UIBarButtonItem(title: "Done", style: .plain, target: self, action: #selector(self.doneTapped))
        let spaceButton = UIBarButtonItem(barButtonSystemItem: .flexibleSpace, target: nil, action: nil)
        let cancelButton = UIBarButtonItem(title: "Cancel", style: .plain, target: self, action: #selector(self.cancelTapped))

        toolBar.setItems([cancelButton, spaceButton, doneButton], animated: false)
        toolBar.isUserInteractionEnabled = true

        self.toolbar = toolBar
    }

    @objc func doneTapped() {
        self.toolbarDelegate?.didTapDone()
    }

    @objc func cancelTapped() {
        self.toolbarDelegate?.didTapCancel()
    }
}

class SwipePriceViewController: UIViewController{
    var diningHallName : String?
    var lowestAsk : Int?
    var highestBid: Int?
    
    @IBOutlet weak var fromTime: UITextField!
    @IBOutlet weak var toTime: UITextField!
    
    var didTapFrom: Bool?

    @IBOutlet weak var lowestAskLabel: UILabel!
    @IBOutlet weak var highestBidLabel: UILabel!
    
    @IBAction func didTapFrom(_ sender: Any) {
        didTapFrom = true
    }
    @IBAction func didTapTo(_ sender: Any) {
        didTapFrom = false
    }
    
    fileprivate let datePickerFrom = ToolbarDatePicker()
    fileprivate let datePickerTo = ToolbarDatePicker()
    
    override func viewDidLoad() {
        super.viewDidLoad()

        lowestAskLabel.text = "$\(lowestAsk)"
        highestBidLabel.text = "$\(highestBid)"
        // Do any additional setup after loading the view.
        var timeFormatter = DateFormatter()
        timeFormatter.dateStyle = DateFormatter.Style.none
        timeFormatter.timeStyle = DateFormatter.Style.short
        self.title = diningHallName
        self.fromTime.inputView = self.datePickerFrom
        self.fromTime.inputAccessoryView = self.datePickerFrom.toolbar
        self.datePickerFrom.datePickerMode = UIDatePicker.Mode.time
        self.datePickerFrom.minuteInterval = 30
        self.datePickerFrom.toolbarDelegate = self
        self.datePickerFrom.minimumDate =  timeFormatter.date(from: "5:00 pm")
        self.datePickerFrom.maximumDate =  timeFormatter.date(from: "7:30 pm")
        self.datePickerFrom.date = timeFormatter.date(from: "5:00 pm")!
        
        fromTime.text = timeFormatter.string(from: timeFormatter.date(from: "5:00 pm")!)
        
        self.toTime.inputView = self.datePickerTo
        self.toTime.inputAccessoryView = self.datePickerFrom.toolbar
        self.datePickerTo.datePickerMode = UIDatePicker.Mode.time
        self.datePickerTo.minuteInterval = 30
        self.datePickerTo.toolbarDelegate = self
        self.datePickerTo.minimumDate =  timeFormatter.date(from: "5:30 pm")
        self.datePickerTo.maximumDate =  timeFormatter.date(from: "8:00 pm")
        self.datePickerTo.date = timeFormatter.date(from: "8:00 pm")!
        
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

extension SwipePriceViewController: ToolbarDatePickerDelegate {

    func didTapDone() {
        var timeFormatter = DateFormatter()
        timeFormatter.dateStyle = DateFormatter.Style.none
        timeFormatter.timeStyle = DateFormatter.Style.short
        
        if (self.didTapFrom!) {
            fromTime.text = timeFormatter.string(from: self.datePickerFrom.date)
            self.datePickerTo.minimumDate = self.datePickerFrom.date.addingTimeInterval(30.0)
            self.fromTime.resignFirstResponder()
            
        } else {
            toTime.text = timeFormatter.string(from: self.datePickerTo.date)
            self.datePickerFrom.maximumDate = self.datePickerTo.date.addingTimeInterval(-30.0)
            self.toTime.resignFirstResponder()
        }
        // TODO: Filter the best ask and bid
    }
    
    func didTapCancel() {
        if(self.didTapFrom!) {
            self.fromTime.resignFirstResponder()
        } else {
            self.toTime.resignFirstResponder()
        }
    }
}
