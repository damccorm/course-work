"""
Names: Daniel McCormick and Angela Burton
Course: CS 4269 Intro to Machine Learning
Project Overview: The code below contains an implementation of the ID3 decision tree algorithm 
and was built by Daniel McCormick, based largely off of the code submitted for the first assignment.
This code was built by Daniel McCormick and Angela Burton.
"""

from math import log
from xlrd import open_workbook
import csv


class Tree_Node:
    # Structure to hold decision tree nodes
    def __init__(self):
        self.feature_name = None
        self.value_list = []
        self.node_list = []
        self.assignment = None
        self.check_prune = True
        self.count = 0


def construct_tree(feature_names, data_instances, depth):
    # INPUTS:
    #   feature_names is a list of features. The target is the last feature
    #   data_instances is a list of lists, where each list is a set of values for features.
    #       Each index corresponds to the feature with the same index in feature_names.
    #       The target is the last value.
    # OUTPUTS:
    #   returns a decision tree splitting on the features
    this_node = Tree_Node()
    if is_perfectly_split(data_instances):
        this_node.assignment = data_instances[0][-1]
        return this_node
    if len(data_instances[0]) == 1 or depth == 0:
        target_map = {}
        for instance in data_instances:
            if instance[-1] in target_map:
                target_map[instance[-1]] += 1
            else:
                target_map[instance[-1]] = 1
        max_feature = None
        max_appearances = 0
        for feature in target_map:
            if target_map[feature] > max_appearances:
                max_appearances = target_map[feature]
                max_feature = feature
        this_node.assignment = max_feature
        return this_node

    # If recursion isn't done, pick best attribute to split on and split data on it
    best_splitting_index = pick_best_attribute(data_instances)
    this_node.feature_name = feature_names[best_splitting_index]
    # copy list so that changes aren't seen further up in recursion
    new_feature_names = list(feature_names)
    del new_feature_names[best_splitting_index]
    for instance in data_instances:
        if instance[best_splitting_index] not in this_node.value_list:
            this_node.value_list.append(instance[best_splitting_index])
    for value in this_node.value_list:
        subset_of_instances = []
        for instance in data_instances:
            if instance[best_splitting_index] == value:
                # copy list so that changes aren't seen further up in recursion
                cur_instance = list(instance)
                del cur_instance[best_splitting_index]
                subset_of_instances.append(cur_instance)
        child_node = construct_tree(new_feature_names, subset_of_instances, depth - 1)
        this_node.node_list.append(child_node)
    return this_node


def pick_best_attribute(data_instances):
    # INPUTS:
    #   data_instances is a list of lists, where each list is a set of values for features.
    #       Each index corresponds to the feature with the same index in feature_names.
    #       The target is the last value.
    # OUTPUTS:
    #   returns the index of the best splitting feature from data_instances
    cur_best_index = 0
    cur_best_entropy = 1
    for i in range(len(data_instances[0]) - 1):
        cur_entropy = 0
        already_seen_values = {}
        for instance in data_instances:
            if instance[i] not in already_seen_values:
                already_seen_values[instance[i]] = True
                cur_entropy += calculate_weighted_entropy(i, instance[i], data_instances)
        if cur_entropy < cur_best_entropy:
            cur_best_entropy = cur_entropy
            cur_best_index = i
    return cur_best_index


def calculate_weighted_entropy(feature_index, feature_value, data_instances):
    # INPUTS:
    #   feature_index is the index of the feature we are calculating entropy for
    #   feature_value is the value of that feature we are calculating entropy for
    #   data_instances is a list of lists, where each list is a set of values for features.
    #       Each index corresponds to the feature with the same index in feature_names.
    #       The target is the last value.
    # OUTPUTS:
    #   returns the weighted entropy for that feature/value.
    num_features_with_value = 0
    classifications = {}
    for instance in data_instances:
        if instance[feature_index] == feature_value:
            num_features_with_value += 1
            if instance[-1] in classifications:
                classifications[instance[-1]] += 1
            else:
                classifications[instance[-1]] = 1
    entropy = 0
    for classification in classifications:
        prob_classification = classifications[classification] / num_features_with_value
        if prob_classification > 0:
            entropy += -1 * prob_classification * log(prob_classification, 2)
    return entropy * num_features_with_value * len(data_instances)


def is_perfectly_split(data_instances):
    # INPUTS:
    #   data_instances is a list of lists, where each list is a set of values for features.
    #       Each index corresponds to the feature with the same index in feature_names.
    #       The target is the last value.
    # OUTPUTS:
    #   returns whether the target_feature is perfectly split
    for i in range(len(data_instances) - 1):
        if data_instances[i][-1] != data_instances[i + 1][-1]:
            return False
    return True


def readcsv(filename):
    # Reads in a csv with the given filename, returns it as a list of lists
    csvlist = []
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            rowlist = []
            rowlist.extend(row)
            csvlist.append(rowlist)
    return csvlist


def print_tree(root, level=1):
    # prints the decision tree stored in the class above
    print("LEVEL ", level)
    if root.assignment is not None:
        print("Assignment:", root.assignment)
    else:
        print("Feature:", root.feature_name)
        print("Check for prune:", root.check_prune)
        for value in root.value_list:
            print("Value:", value)
        for node in root.node_list:
            print_tree(node, level + 1)


def run_tree_against_test_set(root, feature_names, test_set):
    # INPUTS:
    #   root is the root of the decision tree
    #   feature_names is a list of features. The target is the last feature
    #   test_set is a list of lists, where each list is a set of values for features.
    #       Each index corresponds to the feature with the same index in feature_names.
    #       The target is the last value.
    # OUTPUTS:
    #   returns the number of instances that are classified correctly
    correctly_classified = 0
    for instance in test_set:
        if correctly_classify_instance(root, feature_names, instance):
            correctly_classified += 1
            print correctly_classified, instance
    print len(test_set)
    return correctly_classified


def correctly_classify_instance(root, feature_names, instance):
    # INPUTS:
    #   root is the root of the decision tree
    #   feature_names is a list of features. The target is the last feature
    #   instance is a set of values for features.
    #       Each index corresponds to the feature with the same index in feature_names.
    #       The target is the last value.
    # OUTPUTS:
    #   returns whether the tree classifies the instance correctly
    if root.assignment is not None:
        correct = root.assignment == instance[-1]
        if correct:
            root.count += 1  # count is used in pruning the decision tree
        if correct:
            print "TEST", instance[-1]
        return correct
    value = None
    for i in range(len(feature_names)):
        if feature_names[i] == root.feature_name:
            value = instance[i]
    if value is None:
        return False
    for i in range(len(root.value_list)):
        if root.value_list[i] == value:
            return correctly_classify_instance(root.node_list[i], feature_names, instance)


def prune_tree(root, feature_names, validate_instances):
    # INPUT:
    #   root is the root of the decision tree to be pruned
    #   feature_names is a list of features. The target is the last in the list.
    #   validate_instances is the set of validation data
    # OUTPUT:
    #   returns the root of the pruned tree
    correctly_classified = run_tree_against_test_set(root, feature_names, validate_instances)
    to_prune = get_pruning_candidates(root, [])
    for node in to_prune:
        deleted_node = delete_node(node)
        pruned_correctly_classified = run_tree_against_test_set(root, feature_names, validate_instances)
        if pruned_correctly_classified < correctly_classified:
            replace_node(deleted_node, node)
        else:
            correctly_classified = pruned_correctly_classified
        if len(to_prune) == 0:  # if list is empty, find any new candidates
            to_prune = get_pruning_candidates(root, to_prune)
    return root


def replace_node(deleted_node, node):
    # replaces all of node's values with those of deleted_node
    node.feature_name = deleted_node.feature_name
    node.value_list = deleted_node.value_list
    node.node_list = deleted_node.node_list
    node.assignment = deleted_node.assignment
    node.check_prune = False
    node.count = deleted_node.count


def delete_node(node):
    # INPUT:
    #   node is the node of the decision tree that will have its children deleted
    # OUTPUT:
    #   a copy of the deleted node with references to its children
    index = 0
    max_count = 0
    for i in range(len(node.node_list)):
        if node.node_list[i].count > max_count:
            index = i
            max_count = node.node_list[i].count
    deleted_node = copy(node)
    child = node.node_list[index]
    node.feature_name = child.feature_name
    node.value_list = child.value_list
    node.node_list = []
    node.assignment = child.assignment
    node.check_prune = False
    node.count = child.count
    return deleted_node


def copy(node):
    # makes a deep copy of a Tree_Node
    new_node = Tree_Node()
    new_node.feature_name = node.feature_name
    new_node.value_list = node.value_list
    new_node.node_list = node.node_list
    new_node.assignment = node.assignment
    new_node.check_prune = node.check_prune
    new_node.count = node.count
    return new_node


def get_pruning_candidates(root, to_prune):
    # INPUTS:
    #   root is root of the current subtree. Goal is to determine if root should be checked for pruning
    #   to_prune is a dictionary of the form {child : parent}. The child is a candidate to be pruned.
    # OUTPUT:
    #   returns a dictionary of nodes to try to prune
    prune = root.check_prune and len(
        root.node_list) > 0  # the check_prune element ensures we won't check the same node twice
    if prune:
        for child in root.node_list:
            if len(child.node_list) != 0:
                prune = False
                break
        if prune:
            to_prune.append(root)
            root.check_prune = False
        else:
            for child in root.node_list:
                to_prune = get_pruning_candidates(child, to_prune)
    else:
        for child in root.node_list:
            to_prune = gept_pruning_candidates(child, to_prune)
    return to_prune

def read_alzheimers_dataset(sheet):
    # Takes data from sheet and formats it as list of lists with following format:
    # [age, gender, race, apoe4, ventricles, hippocampus, whole brain, mmse, diagnosis]
    # Assumes that columns of sheet are formatted as follows:
    # VISCODE   PTID    AGE PTGENDER    PTRACCAT    DX.bl   APOE4   Ventricles.bl   Hippocampus.bl  WholeBrain.bl   MMSE    PTMARRY
    dataset = []

    for row in range(1, sheet.nrows):
        age = float(sheet.cell(row, 2).value)
        gender = sheet.cell(row, 3).value
        race = sheet.cell(row, 4).value
        diagnosis = sheet.cell(row, 5).value
        apoe4 = int(sheet.cell(row, 6).value)
        ventricles = -1
        if sheet.cell(row, 7).value != "NA":
            ventricles = int(sheet.cell(row, 7).value)
        hippocampus = -1
        if sheet.cell(row, 8).value != "NA":
            hippocampus = int(sheet.cell(row, 8).value)
        whole_brain = -1
        if sheet.cell(row, 9).value != "NA":
            whole_brain = int(sheet.cell(row, 9).value)
        mmse = int(sheet.cell(row, 10).value)

        dataset.append([age, gender, race, apoe4, ventricles, hippocampus, whole_brain, mmse, diagnosis])

    return dataset

def discretize_alzheimers_dataset(instances, num_categories_per_feature):
    # instances is a list of lists, with each list having the following format:
    # [age, gender, race, apoe4, ventricles, hippocampus, whole brain, mmse, diagnosis]
    # Returns the same dataset, but with age, ventricles, hippocampus, whole brain, and mmse discretized

    for j in range(len(instances)):
        instance = instances[j]
        age = float(instance[0])
        ventricles = instance[4]
        hippocampus = instance[5]
        whole_brain = instance[6]
        mmse = instance[7]
        diagnosis = instance[8]

        # Age ranges from 54.4 to 89.6
        bin_size = (89.6-54.4)/num_categories_per_feature
        for i in range(num_categories_per_feature):
            if age >= 54.4 + (i*bin_size) and age <= 54.4 + ((i+1)*bin_size):
                instance[0] = i

        # Ventricles range from 7801 to 145115, also include NA
        bin_size = int((145115-7801)/num_categories_per_feature) + 1
        for i in range(num_categories_per_feature):
            if ventricles >= 7801 + (i*bin_size) and ventricles <= 7801 + ((i+1)*bin_size):
                instance[4] = i

        # Hippocampus range from 3281 to 145115, also include NA
        bin_size = int((145115-3281)/num_categories_per_feature) + 1
        for i in range(num_categories_per_feature):
            if hippocampus >= 3281 + (i*bin_size) and hippocampus <= 3281 + ((i+1)*bin_size):
                instance[5] = i

        # Whole brain ranges from 669364 to 1364689, also include NA
        bin_size = int((1364689-669364)/num_categories_per_feature) + 1
        for i in range(num_categories_per_feature):
            if whole_brain >= 669364 + (i*bin_size) and whole_brain <= 669364 + ((i+1)*bin_size):
                instance[6] = i

        # MMSE ranges from 18 to 30
        bin_size = int((30-18)/num_categories_per_feature) + 1
        for i in range(num_categories_per_feature):
            if mmse >= 18 + (i*bin_size) and mmse <= 18 + ((i+1)*bin_size):
                instance[7] = i        

        if diagnosis != "Alzheimer's" and diagnosis != "AD":
            instance[8] = "NOT"

        instances[i] = instance

    return instances

def construct_tree_with_pruning_option(feature_names, training_instances, depth, with_pruning = False):
    root = None
    if with_pruning:
        validation_size = int(len(training_instances)/5)
        validation_set = training_instances[:validation_size]
        training_set = training_instances[validation_size:]
        root = construct_tree(feature_names, training_set, depth)
        root = prune_tree(root, feature_names, validation_set)
    else:
        root = construct_tree(feature_names, training_instances, depth)
    return root

def main():

    feature_names = ["age", "gender", "race", "apoe4", "ventricles", "hippocampus", "whole brain", "mmse", "marital status", "diagnosis"]
    
    num_of_bins_per_feature = 2
    depth = 8
    pruning = False

    wb = open_workbook("Training_Data.xlsx")
    sheet = wb.sheets()[0]
    training_dataset = read_alzheimers_dataset(sheet)
    wb = open_workbook("Test_Data.xlsx")
    sheet = wb.sheets()[0]
    testing_dataset = read_alzheimers_dataset(sheet)

    training_instances = discretize_alzheimers_dataset(training_dataset, num_of_bins_per_feature)
    testing_instances = discretize_alzheimers_dataset(testing_dataset, num_of_bins_per_feature)

    root = construct_tree_with_pruning_option(feature_names, list(training_instances), depth, pruning)
    correctly_classified = run_tree_against_test_set(root, feature_names, list(testing_instances))
    
    print "Correctly classified", correctly_classified, "out of", len(testing_instances)

if __name__ == "__main__":
    main()

