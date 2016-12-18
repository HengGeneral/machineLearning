# -*- coding: UTF-8 -*-
from math import log

class DecisionTree:

    def __init__(self):
        file = open("lenses.txt")
        self.lens = [inst.strip().split("\t") for inst in file.readlines()]
        self.lensLabel = ['age', 'prescript', 'astigmatic', 'tearRate']

    def create_decision_tree(self):
        tree = self.create_tree(self.lens, self.lensLabel)
        print tree
        return tree

    def majority_count(self, category_list):
        category_count_map = {}
        for item in category_list:
            if item not in category_count_map.keys():
                category_count_map[item] = 0
            category_count_map[item] += 1

        sorted_category_count_map = sorted(category_count_map.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
        return sorted_category_count_map[0][0]

    def cal_entropy(self, data_set):
        number_of_entry = len(data_set)
        label_count = {}
        for instance in data_set:
            current_classify = instance[-1]
            if current_classify not in label_count:
                label_count[current_classify] = 0;
            label_count[current_classify] += 1

        entropy = 0.0
        for key in label_count:
            prob = float(label_count[key]) / number_of_entry
            entropy -= prob * log(prob)

        return entropy

    def split_data_set(self, data_set, index, value):
        ret_data_set = []
        for instance in data_set:
            if instance[index] == value:
                reduce_instance = instance[:index]
                reduce_instance.extend(instance[index+1:])
                ret_data_set.append(reduce_instance)
        return ret_data_set

    def choose_best_property(self, data_set):
        number_of_features = len(data_set[0]) - 1
        base_entropy = self.cal_entropy(data_set)

        best_feature = -1
        best_entropy = 0.0
        best_gain = 0.0
        for feature_index in range(0, number_of_features):
            feature_value_list = [instance[feature_index] for instance in data_set]
            unique_value = set(feature_value_list)
            current_entropy = 0.0
            for value in unique_value:
                sub_data_set = self.split_data_set(data_set, feature_index, value)
                prob = len(sub_data_set) / float(len(data_set))
                current_entropy += prob * self.cal_entropy(sub_data_set)
            info_gain = base_entropy - current_entropy
            if info_gain > best_gain:
                best_gain = info_gain
                best_feature = feature_index

        return best_feature

    def create_tree(self, data_set, labels):
        category_list = [instance[-1] for instance in data_set]
        ##如果分类数全部一致，结点标记为该类，并返回
        if len(category_list) == category_list.count(category_list[0]):
            return category_list[0]

        ##如果只剩下一种分类， 则返回次数出现最多的
        if len(data_set) == 1:
            return majority_count(category_list)

        best_property_index = self.choose_best_property(data_set)
        best_label = labels[best_property_index]
        my_tree = {best_label:{}}
        del(labels[best_property_index])
        feature_values = [instance[best_property_index] for instance in data_set]
        feature_value_set = set(feature_values)
        for value in feature_value_set:
            sub_labels = labels[:]
            my_tree[best_label][value] = self.create_tree(self.split_data_set(data_set, best_property_index, value), sub_labels)

        return my_tree

tree = DecisionTree()
tree.create_decision_tree()

