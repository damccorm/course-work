//
//  University_ParkingTests.swift
//  University ParkingTests
//
//  Created by Thomas Marosz on 11/15/17.
//  Copyright © 2017 PSE. All rights reserved.
//

import XCTest


class University_ParkingTests: XCTestCase {
    var vc: UIViewController!
    
    override func setUp() {
        super.setUp()
        // Put setup code here. This method is called before the invocation of each test method in the class.
        let storyboard = UIStoryboard(name: "Main", bundle: Bundle.main)
        vc = storyboard.instantiateInitialViewController() as! UIViewController
    }
    
    override func tearDown() {
        // Put teardown code here. This method is called after the invocation of each test method in the class.
        super.tearDown()
    }
    
    func testCreateLot() {
        
        // This is an example of a functional test case.
        // Use XCTAssert and related functions to verify your tests produce the correct results.
    }
    
    
    
    func testPerformanceExample() {
        // This is an example of a performance test case.
        self.measure {
            // Put the code you want to measure the time of here.
        }
    }
    
}
