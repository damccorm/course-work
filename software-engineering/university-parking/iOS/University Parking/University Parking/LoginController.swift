//
//  ViewController.swift
//  University Parking
//
//  Created by Thomas Marosz on 11/15/17.
//  Copyright © 2017 PSE. All rights reserved.
//

import UIKit
import Firebase
import FirebaseAuth

class LoginController: UIViewController {

    @IBOutlet weak var UsernameTextField: UITextField!
    @IBOutlet weak var PasswordTextField: UITextField!
    @IBOutlet weak var LoginButton: UIButton!
    
    
    // TODO - authentication
    var loginSuccess = true
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

    @IBAction func attemptLogin(_ sender: Any) {
        let email = self.UsernameTextField.text!
        let password = self.PasswordTextField.text!
        
        if email != "" && password != "" {
            Auth.auth().signIn(withEmail: email, password: password, completion: { (user, error) in
                if error == nil {
                    self.performSegue(withIdentifier: "loginSuccessful", sender: self)
                }
                else {
                    print("error")
                }
            })
        }
        else {
            let alert = UIAlertController(title: "Error", message: "Enter Correct Email/Password", preferredStyle: .alert)
            
            let action = UIAlertAction(title: "OK", style: .default, handler: nil)
            alert.addAction(action)
            self.present(alert, animated: true, completion: nil)
        }
        
    }

}

